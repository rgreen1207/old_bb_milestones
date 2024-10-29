from time import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.config import engine
from app.utilities import SHA224Hash
from app.exceptions import ExceptionHandling
from fastapi_pagination.ext.sqlalchemy import paginate

class BaseActions:

    @staticmethod
    def _add_ordering_to_query(model, query, params):
        """
        Adds ordering to a query based on the specified field and sort order
        :param model(DataModel): The model/table to query
        :param query(select): The initial select statement to augment
        :param order_by(str): The field to sort by
        :param sort(str): The sort order ('ASC' or 'DESC')
        :return: The modified query(select) with the ordering applied
        """
        if "order_by" not in params:
            return query

        model_filter = getattr(model, params["order_by"])
        model_filter = model_filter.desc() if params["sort"] == "DESC" else model_filter.asc()
        return query.order_by(model_filter)

    @staticmethod
    def _filter_query(model, query, params):
        """
        Filters a query based on the specified filters
        :param query(select): The initial select statement to augment
        :param filters(list): The filters to apply
        :return: The modified query(select) with the filters applied
        """
        if "filters" not in params:
            return query

        return query.where(*[getattr(model, k) == v for k, v in params["filters"].items()])

    @staticmethod
    async def delete_without_lookup(item):
        """
        Deleting an item that has been previously looked up and processed inside its respective Model Action file.
        """
        with Session(engine) as session:
            try:
                session.delete(item)
                session.commit()
                return {"ok": True, "Deleted": item}
            except:
                return {"ok": False, "Not Deleted": item}

    @staticmethod
    async def get_one_where(
        model,
        conditions: list,
        check404: bool = True
    ):
        """
        Get one row from the database
        :param model(DataModel): The model/table to query
        :param conditions(list): A list of conditions to match
        :return: A model(DataModel)
        """
        with Session(engine) as session:
            db_item = session.scalars(
                select(model)
                .where(*conditions)
                ).one_or_none()
        if check404:
            await ExceptionHandling.check404(db_item)
        return db_item

    @staticmethod
    async def check_if_exists(model, conditions: list):
        """
        Check if a row exists in the database
        :param model(DataModel): The model/table to query
        :param conditions(list): The conditions to match
        :return: A model(DataModel), or None if no match is found
        """
        with Session(engine) as session:
            return session.scalars(
                select(model)
                .where(*conditions)
                ).one_or_none()

    @staticmethod
    async def check_if_one_exists(model, conditions: list):
        """
        Check if a row exists in the database
        :param model(DataModel): The model/table to query
        :param conditions(list): The conditions to match
        :return: The first model(DataModel) found, or None if no match is found
        """
        with Session(engine) as session:
            return session.scalars(
                select(model)
                .where(*conditions)
                ).first()

    @staticmethod
    def get_one(model, conditions: list):
        """
        Non-Async method to get one row from the database
        :param model(DataModel): The model/table to query
        :param conditions(list): The conditions to match
        :return: A model(DataModel), or None if no match is found
        """
        with Session(engine) as session:
            return session.scalars(
                select(model)
                .where(*conditions)
                ).one_or_none()

    @staticmethod
    async def create(model_objs):
        """
        Create one or more rows in the database for the specified model
        :param model_objs(DataModel instance or list): The model instance(s) to create
        :return: The created model(DataModel instance(s))
        """
        with Session(engine) as session:
            model_objs = model_objs if (is_list := isinstance(model_objs, list)) else [model_objs]

            for obj in model_objs:
                obj.uuid = SHA224Hash() if not obj.uuid else obj.uuid
                obj.time_created = obj.time_updated = int(time())

            session.add_all(model_objs)
            session.commit()

            for obj in model_objs:
                session.refresh(obj)

            return model_objs if is_list else model_objs[0]

    @staticmethod
    async def seed_database(model_objs):
        """
        Create one or more rows in the database for the specified model
        :param model_objs(DataModel instance or list): The model instance(s) to create
        :return: The created model(DataModel instance(s))
        """
        model_objs = model_objs if (is_list := isinstance(model_objs, list)) else [model_objs]

        for obj in model_objs:
            try:
                with Session(engine, expire_on_commit=False) as session:
                    obj.uuid = SHA224Hash() if not obj.uuid else obj.uuid
                    obj.time_created = obj.time_updated = int(time())

                    session.add(obj)
                    session.commit()
            except IntegrityError:
                pass

        return model_objs if is_list else model_objs[0]

    @staticmethod
    async def update(model, conditions: list, updates_obj):
        """
        Update a row in the database for the specified model
        :param model(DataModel): The model/table to update
        :param conditions(list): The conditions to match for the row to update
        :param updates_obj(UpdateModel): The model instance containing the updated fields
        :return: The updated model instance
        """
        with Session(engine) as session:
            db_item = session.scalars(
                select(model)
                .where(*conditions)
                ).one_or_none()
            await ExceptionHandling.check404(db_item)

            updated_fields = updates_obj.dict(exclude_unset=True, exclude_none=True).items()
            for key, value in updated_fields:
                setattr(db_item, key, value)
            db_item.time_updated = int(time())

            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item

    @staticmethod
    async def bulk_update(model, conditions: list, updates_objs, key_list: list):
        """
        Update multiple rows in the database for the specified model
        :param model(DataModel): The model/table to update
        :param conditions(list): The conditions to match for the row to update
        :param updates_obj(UpdateModel): The model instance containing the updated fields
        :return: The updated model instance
        """
        with Session(engine) as session:
            updates = [] #create an empty list for the later to be updated items
            db_items = session.query(model).where(*conditions).filter(model.uuid.in_(key_list)).all() #get each item from the database filtering by the uuids in the key_list
            await ExceptionHandling.check404(db_items, message = "No items found to update")

            items = {} #creating a dictionary of the items from the database
            not_updated = [] #creating an empty list for the items that were not updated
            for db_item in db_items:
                items[db_item.uuid] = db_item #adding each item to the dictionary with the uuid as the key
            for obj in updates_objs:
                if obj.uuid not in items:
                    not_updated.append(obj)
                    continue
                item_from_db = items[obj.uuid]
                update_fields = obj.dict(exclude_unset=True, exclude_none=True).items()
                for key, value in update_fields:
                    setattr(item_from_db, key, value)
                    item_from_db.time_updated = int(time())
                updates.append(item_from_db)

            session.add_all(updates)
            session.commit()
            for i in updates:
                session.refresh(i)
            return {"updated":updates, "not_updated": not_updated}


    @staticmethod
    async def delete_one(model, conditions: list):
        """
        Delete a row from the database for the specified model
        :param model(DataModel): The model/table to delete from
        :param conditions(list): The conditions to match for the row to delete
        :return: The deleted model instance
        """
        with Session(engine) as session:
            db_item = session.scalars(
                select(model)
                .where(*conditions)
                ).one_or_none()
            await ExceptionHandling.check404(db_item)

            try:
                session.delete(db_item)
                session.commit()
                return {"ok": True, "Deleted": db_item}
            except:
                return {"ok": False, "Not Deleted": db_item}

    @staticmethod
    async def delete_all(model, conditions: list):
        """
        Delete all rows from the database for the specified model
        :param model(DataModel): The model/table to delete from
        :param conditions(list): The conditions to match for the rows to delete
        :return: The deletion status and the deleted model object(s)
        """
        with Session(engine) as session:
            db_items = session.scalars(
                select(model)
                .where(*conditions)
                ).all()

            results = []
            for item in db_items:
                try:
                    session.delete(item)
                    results.append({"ok": True, "Deleted": db_items})
                except:
                    results.append({"ok": False, "Not Deleted": db_items})
            session.commit()
            return results

    @classmethod
    async def get_all(
        cls,
        model,
        params: dict,
        check404: bool = True,
        pagination: bool = True
    ):
        """
        Get all rows from the database for a given model/table.

        :param model: The model/table to query.
        :param params: A dictionary of query parameters. Possible parameters include:
            - order_by: The field to sort by, defaults to None.
            - sort: The sort order ('ASC' or 'DESC'), defaults to 'DESC'.
        :param check404: If True, the method will raise a 404 error if no results are found.
        :param pagination: If True, the method will return a paginated response.
        :return: A list of model instances.
        """

        with Session(engine) as session:
            query = select(model)
            query = cls._add_ordering_to_query(model, query, params) if params else query
            query = cls._filter_query(model, query, params) if params else query

            if pagination:
                db_query = paginate(session, query)
                if check404:
                    await ExceptionHandling.check404(db_query.items)
            else:
                db_query = session.scalars(query).all()
                if check404:
                    await ExceptionHandling.check404(db_query)

            return db_query

    @classmethod
    async def get_all_where(
        cls,
        model,
        conditions: list,
        params: dict,
        check404: bool = True,
        pagination: bool = True
    ):
        """
        Get all rows from the database that match the specified conditions
        :param model(DataModel): The model/table to query
        :param conditions(list): A list of conditions to match
        :param params(dict): A dictionary of query parameters
            - order_by(str): The field to sort by
            - sort(str): The sort order ('ASC' or 'DESC')
        :return: A list of model objects, for example [model(DataModel),...]
        """

        with Session(engine) as session:
            query = select(model).where(*conditions)
            query = cls._add_ordering_to_query(model, query, params) if params else query
            query = cls._filter_query(model, query, params) if params else query

            if pagination:
                db_query = paginate(session, query)

            else:
                db_query = session.scalars(query).all()

            if check404:
                message = "No items found matching the specified conditions"
                if pagination:
                    await ExceptionHandling.check404(db_query.items, message=message)
                else:
                    await ExceptionHandling.check404(db_query, message=message)
            return db_query

    @classmethod
    async def update_without_lookup(cls, item, commit:bool = False):
        """
        Committing a change to an item that has been previously looked up and modified inside its respective Model Action file.
        """
        with Session(engine) as session:
            if isinstance(item, list):
                for i in item:
                    i.time_updated = int(time())
                    session.add(i)
                session.commit()
                for i in item:
                    session.refresh(i)
            else:
                item.time_updated = int(time())
                session.add(item)
                session.commit()
                session.refresh(item)
            return item

    # TODO
    # def GetManyByIds(self, table, fields, field, ids=None, orderby=None, orderby_dir='DESC', joiner='and'):
    # async def get_all_wherein(model, field, ids: list, order_by=None, sort='DESC'):
    #   '''
    #   Get all rows from the database
    #   :param model(DataModel): model/table to query
    #   :param conditions(tuple): conditions to match
    #   :param order_by(None|str): the field to sort
    #   :param model(None): model/table to query
    #   :return: returns [model(DataModel),...]
    #   '''
    #   with Session(engine) as session:
    #       query = select(model).where(*conditions)
    #       query = BaseActions._update_query_with_ordering_params(model, query, order_by, sort)
    #       return session.scalars(query).all()

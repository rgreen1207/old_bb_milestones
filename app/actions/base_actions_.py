from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.config import engine
from app.utilities import isList, SHA224Hash, timestampSeconds

class BaseActions:

    @staticmethod
    def _update_query_with_ordering_params(model, query, order_by=None, sort="DESC"):
        """
        Get all rows from the database
        :param model(DataModel): model/table to query
        :param query(select): the initial select statement to augment
        :param order_by(None|str): the field to sort
        :param model(None): model/table to query
        :return: returns query(select)
        """
        if not order_by:
            return query

        modelFilter = getattr(model, order_by)
        modelFilter = modelFilter.desc() if sort == "DESC" else modelFilter.asc()
        return query.order_by(modelFilter)


    @staticmethod
    async def get_all(model, order_by=None, sort="DESC"):
        """
        Get all rows from the database
        :param model(DataModel): model/table to query
        :param order_by(None|str): the field to sort
        :param model(None): model/table to query
        :return: returns [model(DataModel),...]
        """
        with Session(engine) as session:
            query = select(model)
            query = BaseActions._update_query_with_ordering_params(model, query, order_by, sort)
            return session.scalars(query).all()


    @staticmethod
    async def get_all_where(model, conditions: tuple, order_by=None, sort="DESC"):
        """
        Get all rows from the database
        :param model(DataModel): model/table to query
        :param conditions(tuple): conditions to match
        :param order_by(None|str): the field to sort
        :param model(None): model/table to query
        :return: returns [model(DataModel),...]
        """
        with Session(engine) as session:
            query = select(model).where(*conditions)
            query = BaseActions._update_query_with_ordering_params(model, query, order_by, sort)
            return session.scalars(query).all()


    #TODO: 
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


    @staticmethod
    async def get_one_where(model, conditions: tuple):
        """
        Get one row from the database
        :param model(DataModel): model/table to query
        :param conditions(tuple): conditions to match
        :return: returns model(DataModel)
        """
        with Session(engine) as session:
            return session.scalars(
                select(model).where(*conditions)
            ).one_or_none()


    @staticmethod
    async def create(model_objs):
        """
        Get one row from the database
        :param model_obj(DataModel instance): model/table to query
        :return: returns model(DataModel instance)
        """
        print("model_objs:", model_objs)
        objsIsList = isList(model_objs)
        print("objsIsList:", objsIsList)

        with Session(engine) as session:
            objs = [model_objs] if not objsIsList else model_objs

            for obj in objs:
                if not obj.uuid:
                    obj.uuid = SHA224Hash()
                obj.time_created = obj.time_updated = timestampSeconds()
                session.add(obj)

            session.commit()

            for obj in objs:
                session.refresh(obj)

            return objs if not objsIsList else objs[0]


    @staticmethod
    async def update(model, conditions: tuple, update_obj):
        """
        Get one row from the database
        :param model(DataModel): model/table to query
        :param conditions(tuple): conditions to match
        :param model(DataModel): model/table to query
        :return: returns model(DataModel)
        """
        with Session(engine) as session:
            response = session.exec(
                select(model)
                .where(*conditions)
            ).one_or_none()

            if not response:
                return
            
            modelUpdates = update_obj.dict(exclude_unset=True)
            for key, value in modelUpdates.items():
                setattr(response, key, value)
            
            response.time_updated = timestampSeconds()

            session.add(response)
            session.commit()
            session.refresh(response)
            return response


    @staticmethod
    async def delete_one_where(model, conditions: tuple):
        """
        Get one row from the database
        :param model(DataModel): model/table to query
        :param conditions(tuple): conditions to match
        :return: returns bool
        """
        with Session(engine) as session:
            item = session.exec(
                select(model)
                .where(*conditions)
            ).one_or_none()

            if not item:
                raise Exception("item not found")
            
            try:
                session.delete(item)
                session.commit()
                return True
            except:
                return False
                

    @staticmethod
    async def delete_all_where(model, conditions: tuple):
        """
        Get one row from the database
        :param model(DataModel): model/table to query
        :param conditions(tuple): conditions to match
        :return: returns results(dict): 
                    uuid(str): state(bool)
        """
        with Session(engine) as session:
            items = session.exec(
                select(model)
                .where(*conditions)
            ).all()

            if not items:
                raise Exception("items not found")
            
            results = {}
            for item in items:
                try:
                    session.delete(item)
                    results[item.uuid] = True
                except:
                    results[item.uuid] = False
            session.commit()
            return results
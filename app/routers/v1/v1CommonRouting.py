from app.database.config import engine
from sqlalchemy.orm import Session
from app.utilities import SHA224Hash
from sqlalchemy import select
from fastapi import HTTPException
from time import time

class CommonRoutes:

    async def get_all(model):
        with Session(engine) as session:
            items = session.scalars(select(model)).all()
            await ExceptionHandling.check404(items)
            return items

    async def exec_get_all(statement):
        with Session(engine) as session:
            items = session.scalars(statement).all()
            await ExceptionHandling.check404(items)
            return items

    async def exec_get_one(statement):
        with Session(engine) as session:
            response = session.scalars(statement).one_or_none()
            return response

    # Test Implementation of async Sessions, rest of the test code is in db_configs.py
    # from sqlalchemy.orm.ext.asyncio import AsyncSession
    # from sqlalchemy.orm.future import select
    # async def get_all(model):
    #   async with AsyncSession(engine) as session:
    #       items = await session.execute(select(model))
    #       items_list = items.scalars().all()
    #       ExceptionHandling.check404(items_list)
    #       return items_list

    async def get_one(model, search_by):
        with Session(engine) as session:
            item = session.get(model, search_by)
            await ExceptionHandling.check404(item)
            return item

    async def create_one_or_many(items):
        with Session(engine) as session:
            if isinstance(items, list):
                for item in items:
                    item.uuid = SHA224Hash() if item.uuid is None else None
                    item.time_created = item.time_updated = int(time())
                    session.add(item)
            else:
                items.uuid = SHA224Hash() if items.uuid is None else items.uuid
                items.time_created = items.time_updated = int(time())
                session.add(items)

            session.commit()

            if isinstance(items, list):
                for item in items:
                    session.refresh(item)
            else:
                session.refresh(items)
            return items

    async def exec_add_one(item):
        with Session(engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
        return item

    async def update_one(search_by, original_model, update_model):
        with Session(engine) as session:
            db_item = session.get(original_model, search_by)
            await ExceptionHandling.check404(db_item)
            updated_mapped_columns = update_model.dict(exclude_unset=True)
            for key, value in updated_mapped_columns.items():
                setattr(db_item, key, value)
            if hasattr(db_item, "time_updated"):
                db_item.time_updated = int(time())
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item

    async def exec_update(statement, updates):
        with Session(engine) as session:
            response = session.scalars(statement).one_or_none()
            await ExceptionHandling.check404(response)

            updated_mapped_columns = updates.dict(exclude_unset=True)
            for key, value in updated_mapped_columns.items():
                setattr(response, key, value)
            session.add(response)
            session.commit()
            session.refresh(response)
            return response

    async def delete_one(search_by, model):
        with Session(engine) as session:
            item = session.get(model, search_by)
            await ExceptionHandling.check404(item)
            session.delete(item)
            session.commit()
            return {"ok": True, "Deleted:": item}

    async def exec_delete(statement):
        with Session(engine) as session:
            item = session.scalars(statement).one_or_none()
            await ExceptionHandling.check404(item)
            session.delete(item)
            session.commit()
            return {"ok": True, "Deleted:": item}

    async def delete_all(search_by, model):
        with Session(engine) as session:
            items = session.scalars(select(model).where(search_by)).all()
            ExceptionHandling.check404(items)
            for item in items:
                session.delete(item)
            session.commit()
            return {"ok": True, "Deleted:": items}


class ExceptionHandling:

    @staticmethod
    async def check404(item, cron_job: bool = False):
        if cron_job:
            raise Exception("Not Found")
        if not item:
            raise HTTPException(status_code=404, detail="Not Found")

    @staticmethod
    async def custom500(message, cron_job: bool = False):
        if cron_job:
            raise Exception(message)
        raise HTTPException(status_code=500, detail=message)

    @staticmethod
    async def custom405(message, cron_job: bool = False):
        if cron_job:
            raise Exception(message)
        raise HTTPException(status_code=405, detail=message)

# import time as time
# from sqlalchemy.orm.orm import Session
# from sqlalchemy.orm.exc import IntegrityError
# from fastapi import HTTPException
# from src.database.config import get_db

# def see_db():
#   return get_db

# def get_all(db: Session, model_class, skip: int = 0, limit: int = 100):
#   return db.query(model_class).offset(skip).limit(limit).all()

# def get_by_uuid(db: Session, model_class, uuid: str):
#   return db.query(model_class).filter(model_class.uuid == uuid).first()

# def create(db: Session, model_class, schema):
#   instance = model_class(**schema.dict())
#   try:
#       db.add(instance)
#       db.commit()
#       db.refresh(instance)
#   except IntegrityError as e:
#       db.rollback()
#       if "Duplicate entry" in str(e):
#           raise HTTPException(status_code=400, detail="Duplicate entry")
#       raise e
#   return instance

# def update(db: Session, model_class, uuid: str, schema):
#   instance = get_by_uuid(db, model_class, uuid)
#   if instance is None:
#       return None

#   updated_mapped_columns = schema.dict(exclude_unset=True)
#   for key, value in updated_mapped_columns.items():
#       setattr(instance, key, value)

#   if hasattr(instance, 'update_time'):
#       instance.update_time = int(time.time())

#   db.commit()
#   db.refresh(instance)
#   return instance

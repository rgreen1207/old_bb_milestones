import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from app.configs import db_config

# create the database url using values from db_config
DATABASE_URL = f"mysql+pymysql://{db_config.USER}:{db_config.PASSWD}@{db_config.HOST}:{db_config.PORT}/{db_config.DB}"

echo_sql_output: bool = os.environ.get("ENV", "local").lower() == "local"
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=echo_sql_output)

# TODO: refactor logging to use python logging, allowing for more control
#   uncomment the following lines and remove 'echo=True' from engine_create()
#   to enable sqlalchemy logs to go through python logging
# import logging
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

async def get_session():
    with sessionmaker(engine) as session:
        yield session

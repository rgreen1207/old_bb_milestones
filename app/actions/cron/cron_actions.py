from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session
from app.database.config import engine
from sqlalchemy import select
from app.models.clients import ClientUserModelDB
from app.models.users import UserModelDB
from app.routers.v1.v1CommonRouting import ExceptionHandling


rule = {
  "conditions": [
    {
      "var": "hire_anniversary",
      "operator": "=",
      "value": "today"
    },
    {
      "var": "anniversary_value",
      "operator": "=",
      "value": "0"
    }
  ],
  "details": {
    "award_type": "1",
    "client_award": "client_award_uuid",
    "program_award": "program_award_uuid",
    "message": "message_uuid"
  }
}


class CronActions:

    @classmethod
    async def kick_off(cls):
        users = await cls.get_all_cron(UserModelDB)
        client_users = await cls.get_all_cron(ClientUserModelDB)
        client_users_df = pd.DataFrame(client_users)
        users_df = pd.DataFrame(users)
        df = pd.merge(client_users_df, users_df, left_on='user_uuid', right_on='uuid')
        result = await cls.run_rule(df, rule)

        return result

    @classmethod
    async def get_all_cron(cls, model):
        with Session(engine) as session:
            query = select(model)
            db_query = session.scalars(query).all()
            await ExceptionHandling.check404(db_query)
            return db_query

    @classmethod
    async def run_rule(cls, df, rul):
        rule_list = rul["conditions"]

        today = datetime.now()
        today = datetime.fromtimestamp(int(today.timestamp()))

        df["check_day"] = df["time_start"].apply(lambda x: int(datetime.fromtimestamp(x).strftime("%d%m")))
        df["check_year"] = df["time_start"].apply(lambda x: int(datetime.fromtimestamp(x).strftime("%Y")))

        for rule in rule_list:
            match rule["var"]:
                case "hire_anniversary":
                    df = await cls.hire_anniversary(df, rule, today)
                case "anniversary_value":
                    df = await cls.anniversary_value(df, rule, today)
                case _:
                    print("not found")

        return df.to_dict('index')

    @classmethod
    async def hire_anniversary(cls, df, rule, today):
        today_string = today.strftime("%d%m")
        df = df[df["check_day"] == int(today_string)]
        return df

    @classmethod
    async def anniversary_value(cls, df, rule, today):
        year_string = today.strftime("%Y")
        df = df[df["check_year"] == int(year_string)]
        return df

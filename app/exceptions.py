from fastapi import HTTPException


class ExceptionHandling:

    @staticmethod
    async def custom400(message, cron_job: bool = False):
        if cron_job:
            raise Exception(message)
        raise HTTPException(status_code=400, detail=message)

    @staticmethod
    async def check404(item, cron_job: bool = False, message: str = "Not Found"):
        if cron_job:
            raise Exception("Not Found")
        if not item:
            raise HTTPException(status_code=404, detail=message)

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

    @staticmethod
    async def custom409(message, cron_job: bool = False):
        if cron_job:
            raise Exception(message)
        raise HTTPException(status_code=409, detail=message)

    @staticmethod
    async def custom415(message, cron_job: bool = False):
        if cron_job:
            raise Exception(message)
        raise HTTPException(status_code=415, detail=message)

from app.actions.upload import UploadActions


class ClientUploadActions:

    @classmethod
    async def get_upload_url(cls, upload_type, file_name, client_uuid):
        return await UploadActions.generate_upload_url(upload_type, file_name, client_uuid)

    @classmethod
    async def process_roster_file(cls, file_name, client_uuid):
        return await UploadActions.process_csv_file(file_name, client_uuid)

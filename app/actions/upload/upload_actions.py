import io
import csv
import logging
from os import getenv
import boto3
from datadog.api.exceptions import ClientError
from app.exceptions import ExceptionHandling
from app.actions.base_actions import BaseActions
from app.actions.clients.user import ClientUserActions


aws_access_key_id = getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
aws_bucket_name = getenv("AWS_BUCKET_NAME")
role_arn = getenv("AWS_ROLE_ARN")

UPLOAD_TYPE_CONFIG = {
    "roster": {
        "valid_types": ["csv"],
        "path": "/rosters/uploads/"
    },
    "image": {
        "valid_types": ["png", "tiff", "jpeg", "jpg"],
        "path": "/hero_image/"
    },
    "blueboard image": {
        "valid_types": ["png", "tiff", "jpeg", "jpg"],
        "path": "/blueboard/"
    }
}


class UploadActions(BaseActions):

    @staticmethod
    async def get_s3_client():
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        client = session.client("sts")
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="UploadPresignedUrl"
        )

        session = boto3.Session(
            aws_access_key_id=response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
            aws_session_token=response["Credentials"]["SessionToken"]
        )
        client = session.client("sts")
        s3_client = session.client("s3")

        return s3_client

    @staticmethod
    async def verify_upload_file(upload_type, file_name):
        file_type = file_name.split(".")[-1]

        config = UPLOAD_TYPE_CONFIG[upload_type]

        if file_type not in config["valid_types"]:
            await ExceptionHandling.custom415(
                f"File type must be {', '.join(config['valid_types'])}"
            )

        return file_type, config

    @classmethod
    async def generate_upload_url(
        cls,
        upload_type,
        file_name,
        client_uuid,
        award_id=None,
        program_9char=None,
        segment_9char=None
    ):
        file_type, config = await cls.verify_upload_file(upload_type, file_name)

        if upload_type == "roster":
            s3_key = f"/{client_uuid}{config['path']}{file_name}"
        elif upload_type == "image":
            file_parts = [client_uuid]
            if award_id:
                if program_9char:
                    file_parts.append(program_9char)
                    if segment_9char:
                        file_parts.append(segment_9char)
                file_parts.append(f"{award_id}.{file_type}")
            else:
                await ExceptionHandling.custom400("Award ID is required for image uploads")

            s3_key = f"/{'/'.join(file_parts)}"

        return await cls.create_presigned_post(aws_bucket_name, s3_key)

    @classmethod
    async def generate_blueboard_upload_url(cls, award_id, file_name):
        file_type, config = await cls.verify_upload_file("blueboard image", file_name)
        s3_key = f"{config['path']}{award_id}.{file_type}"
        return await cls.create_presigned_post(aws_bucket_name, s3_key)

    @classmethod
    async def create_presigned_post(
        cls,
        bucket_name,
        object_name,
        fields=None,
        conditions=None,
        expiration=100
    ):
        """Generate a presigned URL S3 POST request to upload a file

        :param bucket_name: string
        :param object_name: string
        :param fields: Dictionary of prefilled form fields
        :param conditions: List of conditions to include in the policy
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Dictionary with the following keys:
            url: URL to post to
            fields: Dictionary of form fields and values to submit with the POST
        :return: None if error.
        """

        s3_client = await cls.get_s3_client()

        try:
            response = s3_client.generate_presigned_post(
                bucket_name,
                object_name,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration
            )
        except ClientError as e:
            logging.error(e)
            return None

        return response

    @classmethod
    async def process_csv_file(cls, s3_file_name, client_uuid):
        s3_client = await cls.get_s3_client()

        try:
            response = s3_client.get_object(
                Bucket=aws_bucket_name,
                Key=s3_file_name.file_name
            )
        except ClientError as e:
            logging.error(e)
            return None

        with io.StringIO(response["Body"].read().decode("utf-8")) as stream:
            csv_reader = csv.DictReader(stream, delimiter=",")
            csv_list = [row for row in csv_reader]

        processed_users = [
            await ClientUserActions.create_client_user(user, {"client_uuid": client_uuid}) for user in csv_list
        ]

        return processed_users

    @classmethod
    async def update_hero_image(cls, s3_file_name):
        file_type, _ = cls.verify_upload_file("image", s3_file_name)
        return file_type

    @classmethod
    async def get_hero_image(
        cls,
        hero_image,
        client_uuid,
        award_id,
        program_9char=None,
        segment_9char=None
    ):
        file_type, _ = cls.verify_upload_file("image", hero_image)
        await cls.get_image_path(
            file_type,
            client_uuid,
            award_id,
            program_9char,
            segment_9char
        )
        # TODO: get the file from s3


    @staticmethod
    async def get_image_path(
        file_type,
        client_uuid,
        award_id=None,
        program_9char=None,
        segment_9char=None
    ):
        file_parts = [client_uuid]
        if award_id:
            if program_9char:
                file_parts.append(program_9char)
                if segment_9char:
                    file_parts.append(segment_9char)
            file_parts.append(f"{award_id}.{file_type}")
        else:
            await ExceptionHandling.custom400("Award ID is required")

        s3_key = f"/{'/'.join(file_parts)}"
        return s3_key

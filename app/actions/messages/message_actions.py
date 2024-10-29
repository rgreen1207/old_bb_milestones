import json
from app.actions.awards.awards_actions import AwardActions
from app.routers.v1.dependencies import is_test_mode
from app.actions.clients.client_actions import ClientActions
from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.clients.client_user_models import ClientUserModelDB
from app.models.programs import ProgramModelDB
from app.models.messages import MessageModelDB, MessageCreate, MessageUpdate, MessageSend, MessageRecipient
from app.exceptions import ExceptionHandling
from app.actions.messages.send_message import MessageSendingHandler
from app.actions.users.user_actions import UserActions
from typing import Optional


class MessageActions:

    @staticmethod
    async def get_all(query_params: dict, segment_9char: Optional[str] = None, program_9char: Optional[str] = None):
        return await BaseActions.get_all(MessageModelDB, query_params)

    @staticmethod
    async def get_all_client_messages(client_uuid: str, query_params: dict):
        return await BaseActions.get_all_where(
            MessageModelDB,
            [
                MessageModelDB.client_uuid == client_uuid
            ],
            query_params
        )

    @staticmethod
    async def get_all_program_messages(query_params: dict, path_params: dict):
        return await BaseActions.get_all_where(
            MessageModelDB,
            [
                MessageModelDB.client_uuid == path_params['client_uuid'],
                MessageModelDB.program_9char == path_params['program_9char']
            ],
            query_params
        )

    @staticmethod
    async def get_all_segment_messages(query_params: dict, path_params: dict):
        return await BaseActions.get_all_where(
            MessageModelDB,
            [
                MessageModelDB.client_uuid == path_params['client_uuid'],
                MessageModelDB.program_9char == path_params['program_9char'],
                MessageModelDB.segment_9char == path_params['segment_9char']
            ],
            query_params
        )

    @staticmethod
    async def get_one(message_9char: str, check: bool = True, additional_params: list = None):
        params = [MessageModelDB.message_9char == message_9char]
        if additional_params:
            params.extend(additional_params)
        return await BaseActions.get_one_where(
            MessageModelDB,
            params,
            check
        )

    @classmethod
    async def get_segment_message(cls, message_9char: str, path_params: str):
        return await cls.get_one(
            message_9char,
            True,
            [
                MessageModelDB.client_uuid == path_params['client_uuid'],
                MessageModelDB.program_9char == path_params['program_9char'],
                MessageModelDB.segment_9char == path_params['segment_9char'],
            ]
        )

    @classmethod
    async def get_program_message(cls, message_9char: str, path_params: dict):
        return await cls.get_one(
            message_9char,
            True,
            [
                MessageModelDB.client_uuid == path_params['client_uuid'],
                MessageModelDB.program_9char == path_params['program_9char']
            ]
        )

    @staticmethod
    async def get_program_uuid(program_9char: str, check404: bool = True):
        return await BaseActions.get_one_where(
            ProgramModelDB.uuid,
            [ProgramModelDB.program_9char == program_9char],
            check404
        )

    @staticmethod
    async def check_for_existing_message_by_name(message, throw_error=True):
        existing_message = await BaseActions.check_if_exists(MessageModelDB, [MessageModelDB.name == message.name])
        if existing_message and throw_error:
            await ExceptionHandling.custom405(f"A message with name '{message.name}' already exists.")
        elif existing_message and not throw_error:
            return existing_message
        else:
            return message

    @classmethod
    async def create_segment_message(cls, messages: MessageCreate, segment_9char: str):
        for message in messages:
            message.segment_9char = segment_9char
        return await cls.create_message(messages)

    @classmethod
    async def create_program_message(cls, messages: MessageCreate, program_9char: str):
        for message in messages:
            message.program_9char = program_9char
        return await cls.create_message(messages)

    @classmethod
    async def create_message(cls, messages: MessageCreate, path_params: dict = None):
        if isinstance(messages, list):
            to_create = []
            message_list = []
            for i in messages:
                message = await cls.to_message_model(i)
                i = await cls.add_path_params(i, path_params)
                message = await cls.check_for_existing_message_by_name(message, False)
                if message.uuid is None: #no message with same name exists
                    to_create.append(message)
                else: #message with same name exists, appends message to list and skips a create
                    message_list.append(message)
            if len(to_create) > 0:
                message_list.extend(await BaseActions.create(to_create))
            return message_list
        message = await cls.to_message_model(messages)
        message = await cls.add_path_params(message, path_params)
        message = await cls.check_for_existing_message_by_name(message, False)
        if message.uuid is None:
            return await BaseActions.create(message)
        return message

    @staticmethod
    async def add_path_params(message: MessageCreate, path_params: dict):
        if path_params:
            if 'client_uuid' in path_params:
                message.client_uuid = path_params['client_uuid']
            if 'program_9char' in path_params:
                message.program_9char = path_params['program_9char']
            if 'segment_9char' in path_params:
                message.segment_9char = path_params['segment_9char']
        return message

    @staticmethod
    async def to_message_model(message):
        return MessageModelDB(
            **message.dict(),
            message_9char=await HelperActions.generate_9char()
        )

    @classmethod
    async def update_message(cls, message_9char: str, message_updates: MessageUpdate):
        if message_updates.name:
            await cls.check_for_existing_message_by_name(message_updates, True)

        return await BaseActions.update(
            MessageModelDB,
            [MessageModelDB.message_9char == message_9char],
            message_updates
        )

    @staticmethod
    async def delete_message(message_9char: str):
        message = await BaseActions.get_one_where(MessageModelDB, [MessageModelDB.message_9char == message_9char])
        if message.client_uuid and message.status == 2: #status of 2 indicates "published"
            return await ExceptionHandling.custom405(f"Cannot delete client message {message.name}, status code is published.")
        return await BaseActions.delete_one(
            MessageModelDB, [MessageModelDB.message_9char == message_9char]
        )


    @classmethod
    async def send_message(cls, message_9char: str, send_model: MessageSend):
        return await MessageSendingHandler.send_message({
            "message": await cls.get_one(message_9char),
            "client": await ClientActions.get_client(send_model.client_uuid),
            "recipients": await cls.get_recipient_and_award(send_model.recipients),
        })

    @staticmethod
    async def get_recipient_and_award(recipients: list[MessageRecipient]):
        recipient_list = []

        recipient_client_user_models = await BaseActions.get_all_where(
            ClientUserModelDB,
            [ClientUserModelDB.uuid.in_([recipient.client_user_uuid for recipient in recipients])],
            None,
            False,
            False
        )

        #sorts both lists to be in same order
        recipients = sorted(recipients, key=lambda x: x.client_user_uuid, reverse=True) #sorts incoming recipients by client_user_uuid in reverse order
        recipient_client_user_models = sorted(recipient_client_user_models, key=lambda x: x.uuid, reverse=True) #sorts client_user_models by uuid in reverse order

        for client_user_model in recipient_client_user_models:
            recipient_list.append(
                {
                    "user": await UserActions.get_user(client_user_model.user_uuid, True),
                    "award": await AwardActions.get_award(recipients[recipient_client_user_models.index(client_user_model)].award_uuid),
                    "anniversary": recipients[recipient_client_user_models.index(client_user_model)].anniversary if recipients[recipient_client_user_models.index(client_user_model)].anniversary else None
                }
            )

        return recipient_list



class ClientMessageEventActions:

    async def create_program_event(new_event, request, response):
        event_data = json.loads(new_event.event_data)
        if request.method == "DELETE":
            event_data = event_data['Deleted']
        elif request.method == "POST" and "/send" in request.url.path: #sent messages
            message_9char = request.path_params['message_9char']
            message = await MessageActions.get_one(message_9char)
            new_event.program_9char = message.program_9char if message.program_9char else "system"
            new_event.segment_9char = message.segment_9char if message.segment_9char else None
            new_event.program_uuid = await MessageActions.get_program_uuid(message.program_9char) if message.program_9char else "system"
            new_event.client_uuid = json.loads(request._body.decode("utf-8"))['client_uuid']
            return new_event

        new_event.client_uuid = event_data['client_uuid'] if new_event.client_uuid == None else new_event.client_uuid
        new_event.program_9char = event_data['program_9char'] if event_data['program_9char'] else "system"
        new_event.program_uuid = await MessageActions.get_program_uuid(new_event.program_9char, False) if new_event.program_9char else "system"
        new_event.segment_9char = event_data['segment_9char'] if event_data['segment_9char'] else None
        new_event.program_9char = "test_mesg" if is_test_mode() else new_event.program_9char
        return new_event
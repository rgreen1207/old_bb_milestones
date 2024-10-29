from app.exceptions import ExceptionHandling
from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.programs.program_models import ProgramModelDB
from app.models.programs.program_rule_models import ProgramRuleModelDB


class ProgramRuleActions:

    @staticmethod
    async def get_program_uuid(program_9char: str, check: bool = True):
        return await BaseActions.get_one_where(
            ProgramModelDB.uuid,
            [ProgramModelDB.program_9char == program_9char],
            check
        )

    @staticmethod
    async def get_rule(path_params):
        return await BaseActions.get_one_where(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.rule_9char == path_params["rule_9char"],
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"]
            ]
        )

    @staticmethod
    async def get_all_rules(path_params, query_params):
        return await BaseActions.get_all_where(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"]
            ],
            query_params
            )

    @classmethod
    async def create_rule(cls, rules, path_params, program_uuid):
        if isinstance(rules, list):
            to_create = []
            return_list = []
            rule_models = [ProgramRuleModelDB(
                **rule.dict(),
                program_uuid = program_uuid,
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                rule_9char = await HelperActions.generate_9char()
            ) for rule in rules]
            for rule in rule_models:
                existing_rule = await cls.check_if_rule_exists(path_params, rule.logic)
                if existing_rule:
                    return_list.append(existing_rule)
                else:
                    to_create.append(rule)
            if to_create:
                return_list.extend(await BaseActions.create(to_create))
            return return_list
        else:
            rule_model = ProgramRuleModelDB(
                **rules.dict(),
                program_uuid = program_uuid,
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                rule_9char = await HelperActions.generate_9char()
            )
            existing_rule = await cls.check_if_rule_exists(path_params, rule_model.logic)
            if existing_rule:
                return existing_rule
            return await BaseActions.create(rule_model)

    @classmethod
    async def update_rule(cls, rule_updates, path_params):
        if rule_updates.logic:
            # returns error msg if rule logic already exists
            await cls.check_if_rule_exists(path_params, rule_updates.logic, True)
        return await BaseActions.update(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.rule_9char == path_params["rule_9char"],
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"]
            ],
            rule_updates
        )

    @staticmethod
    async def delete_rule(path_params):
        return await BaseActions.delete_one(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.rule_9char == path_params["rule_9char"],
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"]
            ]
        )

    @classmethod
    async def check_if_rule_exists(cls, path_params: dict, rule_logic: dict, error: bool = False):
        rule = await BaseActions.check_if_exists(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.logic == rule_logic,
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"]
            ]
        )
        if rule and error:
            return await ExceptionHandling.custom409(
                f"Provide program logic already exists for Program {path_params.get('program_9char')}."
            )
        return rule

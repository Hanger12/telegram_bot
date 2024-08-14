from typing import Optional
from database.models import User, Commands, CommandData
import json


def insert_command(user_id, command_name, data: dict) -> None:
    command = Commands.get_or_none((Commands.title == "/" + command_name.split("_")[0]) & (Commands.user == user_id))
    if command is None:
        command = Commands(**data[command_name])
        command.save()


def insert_command_data(user_id, command_name: str, data: dict) -> None:
    command = Commands.get_or_none((Commands.title == "/" + command_name.split("_")[0]) & (Commands.user == user_id))

    if data[command_name]["data"]["platforms"]:
        json_list = json.dumps(data[command_name]["data"]["platforms"])
        data[command_name]["data"]["platforms"] = json_list
    command_data = CommandData(command=command, **data[command_name]["data"])
    command_data.save()


def get_user(user_id) -> Optional[User]:
    return User.get_or_none(User.user_id == user_id)

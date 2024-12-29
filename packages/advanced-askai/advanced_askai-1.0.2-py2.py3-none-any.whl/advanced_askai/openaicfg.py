import json
import os

import keyring  # type: ignore

# from appdirs import user_config_dir  # type: ignore

SERVICE_NAME = "advanced-askai"
# get the current user name
USERNAME = os.getlogin()


def _set_data(data: str) -> None:
    keyring.set_password(SERVICE_NAME, USERNAME, data)


def _get_data() -> str | None:
    return keyring.get_password(SERVICE_NAME, USERNAME)


def save_config(config: dict) -> None:
    data_str = json.dumps(config)
    _set_data(data_str)


def create_or_load_config() -> dict:
    try:
        data = _get_data()
        if data is not None:
            return json.loads(data)
        save_config({})
        return {}
    except OSError:
        save_config({})
        return {}

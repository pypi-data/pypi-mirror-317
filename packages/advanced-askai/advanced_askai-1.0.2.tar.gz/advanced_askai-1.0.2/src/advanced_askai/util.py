import argparse
from getpass import getpass

from advanced_askai.chatgpt import is_valid_api_key
from advanced_askai.openaicfg import create_or_load_config, save_config


def load_or_prompt_for_api_key_and_return_config(args: argparse.Namespace) -> dict:
    config = create_or_load_config()
    if args.set_key:
        if is_valid_api_key(args.set_key):
            config["openai_key"] = args.set_key
            save_config(config)
            config = create_or_load_config()
        else:
            raise ValueError("Invalid OpenAI API key provided.")
    elif "openai_key" not in config:
        while True:
            key = getpass(
                "No OpenAI key found, please enter one now (input will be hidden): "
            )
            if is_valid_api_key(key):
                config["openai_key"] = key
                save_config(config)
                break
            else:
                print("Invalid API key. Please try again.")
    else:
        # Check if the existing key is valid
        if not is_valid_api_key(config["openai_key"]):
            print("Existing API key is invalid. Please enter a new one.")
            while True:
                key = getpass("Enter a valid OpenAI API key: ")
                if is_valid_api_key(key):
                    config["openai_key"] = key
                    save_config(config)
                    break
                else:
                    print("Invalid API key. Please try again.")

    return config


def authenticaion_valid() -> bool:
    config = create_or_load_config()
    return "openai_key" in config and is_valid_api_key(config["openai_key"])


def get_authentication() -> str | None:
    config = create_or_load_config()
    key = config.get("openai_key")
    key = key or None
    return key

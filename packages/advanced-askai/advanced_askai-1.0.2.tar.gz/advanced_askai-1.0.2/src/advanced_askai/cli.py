"""askai - ask openai for help"""

import argparse
import sys

from advanced_askai.chatgpt import (
    ChatGpt,
    ChatGPTAuthenticationError,
    ChatGPTConnectionError,
    ChatGPTRateLimitError,
    get_max_tokens,
)
from advanced_askai.constants import ADVANCED_MODEL, FAST_MODEL
from advanced_askai.internal_chat_session import (
    internal_interactive_chat_session,
    internal_single_chat_session,
)
from advanced_askai.openaicfg import create_or_load_config, save_config
from advanced_askai.parse_args import parse_args
from advanced_askai.prompt_input import prompt_input
from advanced_askai.streams import ConsoleStream, FileOutputStream, MultiStream, Stream
from advanced_askai.util import load_or_prompt_for_api_key_and_return_config


def get_model_max_tokens(args: argparse.Namespace) -> tuple[str, int]:
    max_tokens = args.max_tokens
    model: str
    if args.model is None:
        if args.advanced:
            model = ADVANCED_MODEL
        else:
            model = FAST_MODEL
    else:
        model = args.model

    if max_tokens is None:
        max_tokens = get_max_tokens(model)
    return model, max_tokens


def cli() -> int:
    args = parse_args()
    config = create_or_load_config()
    if args.input_file:
        with open(args.input_file, "r") as file:
            args.prompt = file.read().strip()
    model: str
    max_tokens: int
    model, max_tokens = get_model_max_tokens(args)

    config = load_or_prompt_for_api_key_and_return_config(args)
    key = config["openai_key"]

    prompt = args.prompt

    def log(*pargs, **kwargs):
        if not args.verbose:
            return
        print(*pargs, **kwargs)

    if args.assistant_prompt_file:
        with open(args.assistant_prompt_file, "r") as f:
            ai_assistant_prompt = f.read().strip()
    else:
        ai_assistant_prompt = args.assistant_prompt

    log(prompt)

    chatbot = ChatGpt(
        openai_key=key,
        max_tokens=max_tokens,
        model=model,
        ai_assistant_prompt=ai_assistant_prompt,
    )

    streams: list[Stream] = [ConsoleStream()]
    if args.output:
        streams.append(FileOutputStream(args.output))
    outstream = MultiStream(streams)

    try:
        interactive = prompt is None
        if not interactive:
            internal_single_chat_session(
                chatbot=chatbot,
                prompts=[prompt],
                outstream=outstream,
                as_json=args.json,
                check=args.check,
                no_stream=args.no_stream,
                status_print_func=print,
            )
            return 0
        print(
            "\nInteractive mode - press return three times to submit your code to OpenAI"
        )
        internal_interactive_chat_session(
            chatbot=chatbot,
            prompts=[],
            outstream=outstream,
            as_json=args.json,
            no_stream=args.no_stream,
            check=args.check,
            prompt_input_func=prompt_input,
            status_print_func=print,
        )
    except ChatGPTConnectionError as err:
        print(err)
        return 1
    except ChatGPTAuthenticationError as e:
        print(
            "Error authenticating with OpenAI, deleting password from config and exiting."
        )
        print(e)
        save_config({})
        return 1
    except ChatGPTRateLimitError:
        print("Rate limit exceeded, set a new key with --set-key")
        return 1
    return 0


def main() -> int:
    try:
        return cli()
    except KeyboardInterrupt:
        return 1
    except SystemExit as e:
        if isinstance(e.code, int):
            return e.code
        return 1


if __name__ == "__main__":
    sys.exit(main())

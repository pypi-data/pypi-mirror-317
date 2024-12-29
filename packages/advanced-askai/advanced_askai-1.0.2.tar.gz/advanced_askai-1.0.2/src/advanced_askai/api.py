from typing import Callable

from advanced_askai.internal_chat_session import (
    internal_interactive_chat_session,
    internal_single_chat_session,
)
from advanced_askai.make_chatbot import make_chatbot
from advanced_askai.prompt_input import prompt_input
from advanced_askai.streams import ConsoleStream, NullOutStream, Stream
from advanced_askai.types import ChatBotConfig


def chat_session(
    chat_config: ChatBotConfig,
    prompts: list[str] | None = None,
    outstream: Stream | None = None,
    as_json: bool = False,
    no_stream: bool = False,
    check: bool = False,
    status_print_func: Callable[[str], None] = print,
) -> None:
    """Runs a single chat query, throws exceptions if there are issues"""
    prompts = prompts or []
    outstream = outstream or ConsoleStream()
    chatbot = make_chatbot(chat_config)
    return internal_interactive_chat_session(
        chatbot=chatbot,
        prompts=prompts,
        outstream=outstream,
        as_json=as_json,
        no_stream=no_stream,
        check=check,
        status_print_func=status_print_func,
        prompt_input_func=prompt_input,
    )


def single_query(
    chat_config: ChatBotConfig,
    prompt: str | list[str],
    outstream: Stream | None = None,
    as_json: bool = False,
    no_stream: bool = False,
    check: bool = False,
    status_print_func: Callable[[str], None] = print,
) -> str:
    """Runs a single chat query, throws exceptions if there are issues"""
    chatbot = make_chatbot(chat_config)
    outstream = outstream or ConsoleStream()
    if isinstance(prompt, str):
        prompts = [prompt]
    else:
        prompts = prompt
    return internal_single_chat_session(
        chatbot=chatbot,
        prompts=prompts,
        outstream=outstream,
        as_json=as_json,
        no_stream=no_stream,
        check=check,
        status_print_func=status_print_func,
    )


class Chat:
    def __init__(
        self,
        chat_config: ChatBotConfig,
        chat_history: list[str] | None = None,
        outstream: Stream | None = None,
        as_json: bool = False,
        no_stream: bool = False,
        check: bool = False,
        status_print_func: Callable[[str], None] = print,
    ) -> None:
        self.chat_config = chat_config
        self.prompts = chat_history if chat_history is not None else []
        self.outstream = outstream or NullOutStream()
        self.as_json = as_json
        self.no_stream = no_stream
        self.check = check
        self.status_print_func = status_print_func

    def query(self, prompt: str) -> str:
        self.prompts.append(prompt)
        response_text = single_query(
            chat_config=self.chat_config,
            prompt=prompt,
            outstream=self.outstream,
            as_json=self.as_json,
            no_stream=self.no_stream,
            check=self.check,
            status_print_func=self.status_print_func,
        )
        self.prompts.append(response_text)
        return response_text

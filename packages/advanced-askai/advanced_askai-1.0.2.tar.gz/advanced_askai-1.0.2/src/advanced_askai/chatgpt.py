# mypy: disable-error-code="attr-defined,valid-type"

"""Interacts with open ai's chat bot."""


import threading
from typing import Any, Optional

import json5 as json
import openai
import tiktoken
from openai import APIConnectionError, AuthenticationError, BadRequestError, OpenAI

from advanced_askai.constants import ADVANCED_MODEL, HIDDEN_PROMPT_TOKEN_COUNT


def is_valid_api_key(api_key: str) -> bool:
    """
    Test whether the given OpenAI API key is valid.

    :param api_key: The OpenAI API key to test
    :return: True if the key is valid, False otherwise
    """
    client = OpenAI(api_key=api_key)
    try:
        # Attempt to list models, which requires a valid API key
        client.models.list()
        return True
    except AuthenticationError:
        return False
    except (APIConnectionError, BadRequestError):
        # If there's a connection error or bad request, we can't determine if the key is valid
        raise


def get_max_tokens(model: str) -> int:
    if model == ADVANCED_MODEL:
        return 4096
    return 16384


class ChatGPTConnectionError(BaseException):
    def __init__(self, conn_error: APIConnectionError):
        super().__init__(conn_error)
        self.err = conn_error


class ChatGPTAuthenticationError(BaseException):
    def __init__(self, auth_error: AuthenticationError):
        super().__init__(auth_error)
        self.err = auth_error


class ChatGPTRateLimitError(BaseException):
    def __init__(self, rate_error: openai.RateLimitError):
        super().__init__(rate_error)
        self.err = rate_error


ChatCompletion = openai.ChatCompletion  # pylint: disable=no-member


# Create a thread-safe dictionary to store OpenAI client instances
client_instances_lock = threading.Lock()
client_instances: dict[str, openai.OpenAI] = {}


def get_client_instance(openai_key: str) -> OpenAI:
    with client_instances_lock:
        if openai_key not in client_instances:
            client_instances[openai_key] = openai.OpenAI(api_key=openai_key)
        out = client_instances[openai_key]
        assert out is not None
        return out


def count_tokens(model: str, text: str):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


def ai_query(
    openai_key: str,
    prompts: list[str],
    max_tokens: int,
    model: str,
    ai_assistant_prompt: str,
) -> ChatCompletion:

    # assert prompts is odd
    assert (
        len(prompts) % 2 == 1
    )  # Prompts alternate between user message and last response
    if max_tokens < 0:
        # take corrective action.
        max_tokens = 16000  # override it and just send something big.
    messages = [
        {
            "role": "system",
            "content": ai_assistant_prompt,
        },
    ]
    for i, prompt in enumerate(prompts):
        if i % 2 == 0:
            messages.append({"role": "assistant", "content": prompt})
        else:
            messages.append({"role": "user", "content": prompt})

    # Use the get_client_instance function to ensure thread safety
    client = get_client_instance(openai_key)

    # compute the max_tokens by counting the tokens in the prompt
    # and subtracting that from the max_tokens
    messages_json_str = json.dumps(messages)
    prompt_tokens = count_tokens(model, messages_json_str)
    max_tokens = max_tokens - prompt_tokens - HIDDEN_PROMPT_TOKEN_COUNT
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0,
            stream=True,
        )
        return response
    except APIConnectionError as e:
        raise ChatGPTConnectionError(e)
    except AuthenticationError as e:
        raise ChatGPTAuthenticationError(e)


class ChatStream:
    def __init__(self, chatcompletion: ChatCompletion, no_stream: bool = False):
        self.chatcompletion = chatcompletion
        self.no_stream = no_stream

    def success(self) -> bool:
        return self.chatcompletion.response.is_success

    def response(self) -> Any:
        return self.chatcompletion.response

    def __iter__(self):
        all_str = ""
        for event in self.chatcompletion:
            choice = event.choices[0]
            delta = choice.delta
            event_text = delta.content
            if event_text is None:
                break
            if not self.no_stream:
                yield event_text
            else:
                all_str += event_text
        if self.no_stream:
            yield all_str


class ChatGpt:
    def __init__(
        self,
        openai_key: str,
        model: str,
        ai_assistant_prompt: str,
        max_tokens: int | None = None,
    ):
        self.openai_key = openai_key
        self.model = model
        self.max_tokens = max_tokens or get_max_tokens(model)
        self.ai_assistant_prompt = ai_assistant_prompt

    def query(
        self,
        prompts: list[str],
        max_tokens: Optional[int] = None,
        no_stream: bool = False,
    ) -> ChatStream:
        chat_completion = ai_query(
            openai_key=self.openai_key,
            prompts=prompts,
            max_tokens=max_tokens or self.max_tokens,
            model=self.model,
            ai_assistant_prompt=self.ai_assistant_prompt,
        )
        return ChatStream(chat_completion, no_stream)

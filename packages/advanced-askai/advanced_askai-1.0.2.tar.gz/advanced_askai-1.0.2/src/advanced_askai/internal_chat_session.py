import os
from typing import Callable

from advanced_askai.chatgpt import ChatGpt
from advanced_askai.constants import AI_ASSISTANT_CHECKER_PROMPT
from advanced_askai.run_chat_query import run_chat_query
from advanced_askai.streams import NullOutStream, Stream


def internal_iterate_chat_session(
    chatbot: ChatGpt,
    prompts: list[str],
    outstream: Stream,
    as_json: bool,
    no_stream: bool,
    check: bool,
    status_print_func: Callable[[str], None],
) -> str:
    """Runs a single chat query, throws exceptions if there are issues"""
    assert len(prompts) % 2 == 1, "Prompt count should be odd"
    response_text = run_chat_query(
        chatbot=chatbot,
        prompts=prompts,
        outstream=NullOutStream() if check else outstream,
        as_json=as_json,
        no_stream=no_stream,
        print_status=True,
    )
    if not check:
        return response_text
    prompts.append(response_text)
    check_prompt = AI_ASSISTANT_CHECKER_PROMPT + "\n\n" + prompts[-1]
    prompts.append(check_prompt)
    status_print_func("\n############ CHECKING RESPONSE")
    response_text = run_chat_query(
        chatbot=chatbot,
        prompts=prompts,
        outstream=outstream,
        as_json=as_json,
        no_stream=no_stream,
        print_status=False,
    )
    return response_text


def internal_single_chat_session(
    chatbot: ChatGpt,
    prompts: list[str],
    outstream: Stream,
    as_json: bool,
    no_stream: bool,
    check: bool,
    status_print_func: Callable[[str], None],
) -> str:
    """Runs a single chat query, throws exceptions if there are issues"""
    return internal_iterate_chat_session(
        chatbot=chatbot,
        prompts=prompts,
        outstream=outstream,
        as_json=as_json,
        no_stream=no_stream,
        check=check,
        status_print_func=status_print_func,
    )


def internal_interactive_chat_session(
    chatbot: ChatGpt,
    prompts: list[str],
    outstream: Stream,
    as_json: bool,
    no_stream: bool,
    check: bool,
    prompt_input_func: Callable[[], str],
    status_print_func: Callable[[str], None],
) -> None:
    """Runs a chat query, throws exceptions if there are issues"""
    assert (
        len(prompts) % 2 == 0
    ), "Pre-populated prompts (indicating previous history) should be even"

    while True:
        next_prompt = prompt_input_func()
        prompts.append(next_prompt)
        new_cmd = prompts[-1].strip().replace("()", "")
        if new_cmd.startswith("!"):
            prompts = prompts[0:-1]
            new_cmd = new_cmd[1:]
            rtn = os.system(new_cmd)
            status_print_func(f"Command exited and returned {rtn}")
            next_prompt = prompt_input_func()
            prompts.append(next_prompt)
            continue
        elif new_cmd == "exit":
            status_print_func("Exited due to 'exit' command")
            return
        assert len(prompts) % 2 == 1, "Prompt count should be odd"
        response_text = internal_iterate_chat_session(
            chatbot=chatbot,
            prompts=prompts,
            outstream=outstream,
            as_json=as_json,
            no_stream=no_stream,
            check=check,
            status_print_func=status_print_func,
        )
        prompts.append(response_text)

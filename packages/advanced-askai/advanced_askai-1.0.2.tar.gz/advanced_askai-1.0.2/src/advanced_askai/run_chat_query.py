"""askai - ask openai for help"""

from advanced_askai.chatgpt import ChatGpt, ChatStream
from advanced_askai.streams import Stream


def run_chat_query(
    chatbot: ChatGpt,
    prompts: list[str],
    outstream: Stream,
    as_json: bool,
    no_stream: bool,
    print_status: bool,
) -> str:
    """Runs a chat query, throws exceptions if there are issues. Returns the response text."""
    if not as_json:
        if print_status:
            print("############ OPEN-AI QUERY")
    chat_stream: ChatStream = chatbot.query(prompts, no_stream=no_stream)
    if as_json:
        return str(chat_stream)

    if chat_stream is None or not chat_stream.success():
        if print_status:
            print("No error response received from OpenAI, response was:")
        outstream.write(str(chat_stream.response()))
        raise Exception("No response from OpenAI")

    if print_status:
        print("############ OPEN-AI RESPONSE\n")
    response_text = ""
    for text in chat_stream:
        if text is None:
            break
        response_text += text
        outstream.write(text)
    outstream.write("\n\n")

    # return None
    return response_text

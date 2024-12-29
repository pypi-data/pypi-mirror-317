from advanced_askai.chatgpt import ChatGpt
from advanced_askai.types import ChatBotConfig


def make_chatbot(config: ChatBotConfig) -> ChatGpt:
    return ChatGpt(
        openai_key=config.api_key,
        model=config.model,
        ai_assistant_prompt=config.ai_assistant_prompt,
        max_tokens=config.max_tokens,
    )

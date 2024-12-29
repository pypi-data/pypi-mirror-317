from dataclasses import dataclass


@dataclass
class ChatBotConfig:
    model: str
    api_key: str
    ai_assistant_prompt: str
    max_tokens: int | None = None

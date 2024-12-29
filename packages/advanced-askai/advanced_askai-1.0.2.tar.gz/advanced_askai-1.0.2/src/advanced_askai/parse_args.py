import argparse

from advanced_askai.constants import ADVANCED_MODEL, AI_ASSISTANT


def parse_args() -> argparse.Namespace:
    argparser = argparse.ArgumentParser(usage="Ask OpenAI for help with code")
    argparser.add_argument("prompt", help="Prompt to ask OpenAI", nargs="?")
    argparser.add_argument(
        "--input-file", help="Input file containing prompts", type=str
    )
    argparser.add_argument("--json", help="Print response as json", action="store_true")
    argparser.add_argument("--set-key", help="Set OpenAI key")
    argparser.add_argument("--output", help="Output file", type=str)
    model_group = argparser.add_mutually_exclusive_group()
    model_group.add_argument(
        "--advanced",
        action="store_true",
        default=False,
        help=f"bleeding edge model: {ADVANCED_MODEL}",
    )
    model_group.add_argument("--model", default=None)
    argparser.add_argument("--verbose", action="store_true", default=False)
    argparser.add_argument("--no-stream", action="store_true", default=False)
    argparser.add_argument("--assistant-prompt", type=str, default=AI_ASSISTANT)
    argparser.add_argument(
        "--assistant-prompt-file", type=str, help="File containing assistant prompt"
    )
    # max tokens
    argparser.add_argument(
        "--max-tokens", help="Max tokens to return", type=int, default=None
    )
    argparser.add_argument(
        "--code",
        action="store_true",
        default=False,
        help="Code mode: enables aider mode",
    )
    argparser.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Sends the response back to the chatbot for a second opinion",
    )
    return argparser.parse_args()

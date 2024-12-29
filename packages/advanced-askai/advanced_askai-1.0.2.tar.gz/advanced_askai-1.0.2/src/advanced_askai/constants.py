HIDDEN_PROMPT_TOKEN_COUNT = (
    100  # this hack corrects for the unnaccounted for tokens in the prompt
)
ADVANCED_MODEL = "gpt-4o"
FAST_MODEL = "gpt-4o-mini"

AI_ASSISTANT = (
    "You are a helpful assistant to a senior programmer. "
    "If I am asking how to do something in general then go ahead "
    "and recommend popular third-party apps that can get the job done, "
    "but don't recommend additional tools when I'm currently asking how to do use "
    "a specific tool."
)

AI_ASSISTANT_CHECKER_PROMPT = (
    "Now check this answer and verify if it's correct. You will look at the question asked and\n"
    "check that the answer matches the exact specifications. If it's correct, say so. \n"
    "If it's not correct or if there are any issues, explain what's wrong and provide the correct information. \n"
    "Otherwise, say that this correct and repeat the answer VERBATIM.\n"
    'Do not provide any additional information, such as "This is correct." or "This is incorrect.", just provide the correct information.'
)

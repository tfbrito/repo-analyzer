import os

from openai import OpenAI

from .prompts import SYSTEM_PROMPT, build_user_prompt

DEFAULT_MODEL = "anthropic/claude-sonnet-4"


def analyze(context: dict, model: str = DEFAULT_MODEL) -> str:
    """Send collected context to LLM via OpenRouter and return the Markdown report."""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(context)},
        ],
        max_tokens=4096,
    )

    return response.choices[0].message.content

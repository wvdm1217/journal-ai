from typing import Optional

from openai import OpenAI

from journal_ai.config import Config


def generate_title(content: str, config: Optional[Config] = None) -> str:
    if config is None:
        config = Config.from_env()

    client = OpenAI(api_key=config.openai_api_key)

    prompt = (
        "Generate a short, engaging title (max 5 words) for this journal entry:\n\n"
        f"{content}"
    )

    try:
        response = client.chat.completions.create(
            model=config.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip('" \n')
    except Exception as e:
        print(f"Error generating title: {str(e)}")
        return "Untitled Entry"

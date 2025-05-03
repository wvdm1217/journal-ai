from typing import Optional

from openai import OpenAI

from journal_ai.config import Config


def generate_title(content: str, config: Optional[Config] = None) -> str:
    """
    Generate a title for the journal entry using OpenAI's API.
    Args:
        content (str): The content of the journal entry.
        config (Optional[Config]): Configuration object containing API key and model.
    Returns:
        str: The generated title.
    """
    if config is None:
        config = Config.from_env()

    if config.openai_api_key:
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
            output = response.choices[0].message.content
            if output:
                return output.strip('" \n')
            else:
                return "Untitled Entry"
        except Exception as e:
            print(f"Error generating title: {str(e)}")
            return "Untitled Entry"
    else:
        return "Untitled Entry"

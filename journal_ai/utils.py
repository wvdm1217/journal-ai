from typing import List, Optional

from openai import OpenAI
from pydantic import BaseModel, Field

from journal_ai.config import Config
from journal_ai.logger import logger


class Tags(BaseModel):
    tags: List[str] = Field(
        description="A list of tags of entities and actions in the text."
    )


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
            f"Generate a short title (max 5 words) for this journal entry:\n\n{content}"
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


def generate_tags(content: str, config: Optional[Config] = None) -> List[str]:
    """
    Generate tags for the journal entry using OpenAI's API.
    Args:
        content (str): The content of the journal entry.
    Returns:
        List[str]: The generated tags.
    """

    if config is None:
        config = Config.from_env()
    if config.openai_api_key:
        prompt = """Generate a list of tags for journal entries.
        The tags can include entities and actions.
        The tags should not include adjectives or adverbs."""

        messages = [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": content,
            },
        ]
        try:
            client = OpenAI(api_key=config.openai_api_key)

            response = client.beta.chat.completions.parse(
                model=config.model,
                messages=messages,  # type: ignore
                response_format=Tags,
            )

            parsed_response = response.choices[0].message.parsed
            if not parsed_response:
                return []
            if isinstance(parsed_response, Tags):
                return parsed_response.tags
            else:
                raise ValueError(f"Unexpected response format: {type(parsed_response)}")
        except Exception as e:
            logger.error(f"Error generating tags: {str(e)}")
            return []
    else:
        return []


if __name__ == "__main__":
    # Example usage
    content = "The dog barked loudly at the mailman, Dave."
    config = Config.from_env()
    title = generate_title(content, config)
    tags = generate_tags(content, config)
    print(f"Generated Title: {title}")
    print(f"Generated Tags: {tags}")

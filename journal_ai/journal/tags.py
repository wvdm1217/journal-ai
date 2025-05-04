import re
from typing import List


def generate_tags(content: str) -> List[str]:
    """Generate tags from content that use @ to indicate a tag.

    Args:
        content (str): The content from which to generate tags.

    Returns:
        List[str]: A list of generated tags.

    Example:
        >>> content = "This is a test journal entry with tags @journal @writing @test."
        >>> generate_tags(content)
        ['journal', 'writing', 'test']
        >>> content = "No tags here"
        >>> generate_tags(content)
        []
        >>>
    """
    # Find all @ followed by word characters, then filter for valid tags
    tag_pattern = r"(\s|^)@(\w+)(?=\s|[.,!?;:]|$)"
    matches = re.findall(tag_pattern, content)

    # Extract just the tag name from each match (second group)
    tags = [match[1] for match in matches]

    return tags


if __name__ == "__main__":
    # Example usage
    content = "This is a test journal entry with tags @journal @writing @test."
    print(generate_tags(content))  # Output: ['journal', 'writing', 'test']

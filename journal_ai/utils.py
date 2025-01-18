from openai import OpenAI
import os


def generate_title(content: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"Generate a short, engaging title (max 5 words) for this journal entry:\n\n{
        content}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.7
        )
        return response.choices[0].message.content.strip('" \n')
    except Exception as e:
        return "Untitled Entry"

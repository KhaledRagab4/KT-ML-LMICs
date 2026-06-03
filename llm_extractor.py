import os

from dotenv import load_dotenv
from openai import OpenAI


MODEL = "gpt-5.5"


def get_openai_client():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add it to your .env file."
        )

    return OpenAI()


def test_openai_connection():
    client = get_openai_client()

    response = client.responses.create(
        model=MODEL,
        input="Reply with exactly: OpenAI connection works",
    )

    print(response.output_text)


def build_extraction_prompt(article):
    title = article.get("title", "")
    abstract = article.get("abstract", "")

    prompt = f"""
You are helping extract structured implementation evidence from a PubMed article.

Return concise JSON with these fields:
- implementation_study: true or false
- study_design: short string
- barriers: list of strings
- facilitators: list of strings
- setting: short string
- reason: short explanation

Title:
{title}

Abstract:
{abstract}
"""

    return prompt.strip()


if __name__ == "__main__":
    test_openai_connection()
import os

from dotenv import load_dotenv
from google import genai


MODEL = "gemini-3.5-flash"


def get_gemini_client():
    """
    Load GEMINI_API_KEY from .env and create a Gemini client.
    """
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def test_gemini_connection():
    """
    Small connection test before adding Gemini to the real pipeline.
    """
    client = get_gemini_client()

    response = client.models.generate_content(
        model=MODEL,
        contents="Reply with exactly: Gemini connection works",
    )

    print(response.text.strip())


def build_extraction_prompt(article):
    """
    Build a future extraction prompt for a PubMed article.
    We are not using it in the pipeline yet.
    """
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

Important rules:
- Do not invent information.
- If something is missing, write "not reported".
- Base your answer only on the title and abstract.

Title:
{title}

Abstract:
{abstract}
"""

    return prompt.strip()


if __name__ == "__main__":
    test_gemini_connection()
import json
import os

from dotenv import load_dotenv
from google import genai


MODEL = "gemini-3.5-flash"
RAW_ARTICLES_PATH = "data/raw_pubmed_articles.jsonl"


def get_gemini_client():
    """
    Load GEMINI_API_KEY from .env and create a Gemini client.
    """
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    return genai.Client(api_key=api_key)


def clean_llm_json(raw_text):
    """
    Clean common LLM JSON formatting issues, then parse the text as JSON.
    """
    text = raw_text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1).strip()

    if text.startswith("```"):
        text = text.replace("```", "", 1).strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print("Could not parse Gemini output:")
        print(raw_text)
        return None


def load_raw_articles(path=RAW_ARTICLES_PATH, limit=5):
    """
    Load a small number of raw PubMed articles from a JSONL file.
    JSONL means one JSON object per line.
    """
    articles = []

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Could not find {path}. Run python run_pipeline.py first."
        )

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            article = json.loads(line)
            articles.append(article)

            if len(articles) >= limit:
                break

    return articles


def build_screening_prompt(article):
    """
    Build a screening prompt for Gemini.
    The goal is to decide whether the abstract is implementation / KT evidence.
    """
    title = article.get("title", "")
    abstract = article.get("abstract", "")

    prompt = f"""
You are screening PubMed abstracts for implementation science / knowledge translation evidence in LMICs.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations outside JSON.

Inclusion criteria:
Include if the abstract describes a real implementation or knowledge translation activity, such as:
- guideline implementation
- evidence-based practice implementation
- quality improvement with an implementation strategy
- scale-up of a health intervention
- implementation support, training, audit-feedback, supervision, or facilitation
- health system implementation program

Exclusion criteria:
Exclude if it is only:
- prevalence or risk factor study
- purely clinical outcome study
- systematic review or scoping review
- protocol only
- editorial or commentary
- theoretical framework only
- not LMIC-related
- insufficient abstract

Return this JSON schema exactly:

{{
  "decision": "include | exclude | uncertain",
  "reason": "one sentence",
  "exclusion_category": "systematic_review | protocol_only | theoretical_framework | editorial | clinical_only | epidemiology_only | insufficient_abstract | non_lmic | other | null",
  "confidence": "high | medium | low"
}}

Title:
{title}

Abstract:
{abstract}
"""
    return prompt.strip()


def screen_article_with_gemini(client, article):
    """
    Send one article to Gemini and return a screening decision dictionary.
    """
    prompt = build_screening_prompt(article)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return clean_llm_json(response.text)


def main():
    """
    Run Gemini screening on the first 5 raw PubMed articles.
    """
    client = get_gemini_client()
    articles = load_raw_articles(limit=5)

    print("Gemini screening batch test")
    print("=" * 40)

    included_count = 0
    excluded_count = 0
    uncertain_count = 0

    for index, article in enumerate(articles, start=1):
        pmid = article.get("pmid", "not reported")
        title = article.get("title", "not reported")

        decision = screen_article_with_gemini(client, article)

        print(f"\nArticle {index}")
        print("-" * 40)
        print(f"PMID: {pmid}")
        print(f"Title: {title}")

        if decision is None:
            print("Decision: could not parse Gemini output")
            uncertain_count += 1
            continue

        decision_label = decision.get("decision", "uncertain")

        if decision_label == "include":
            included_count += 1
        elif decision_label == "exclude":
            excluded_count += 1
        else:
            uncertain_count += 1

        print(f"Decision: {decision_label}")
        print(f"Reason: {decision.get('reason')}")
        print(f"Exclusion category: {decision.get('exclusion_category')}")
        print(f"Confidence: {decision.get('confidence')}")

    print("\nSummary")
    print("=" * 40)
    print(f"Included: {included_count}")
    print(f"Excluded: {excluded_count}")
    print(f"Uncertain: {uncertain_count}")


if __name__ == "__main__":
    main()
import json
import os
from datetime import date

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
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def clean_llm_json(raw_text):
    """
    Clean common LLM JSON problems and convert text into a Python dictionary.
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
        print("Could not parse JSON. Raw model output:")
        print(raw_text)
        return None


def build_extraction_prompt(article):
    """
    Build a prompt for extracting structured implementation evidence.
    Gemini should focus on analytical fields, not trusted metadata.
    """
    title = article.get("title", "")
    abstract = article.get("abstract", "")

    prompt = f"""
You are extracting structured implementation evidence from a PubMed abstract.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations outside JSON.

Rules:
- Use only the title and abstract.
- Do not invent missing information.
- If a field is missing, write "not reported".
- If you are unsure, use extraction_confidence = "low".

Return exactly this JSON schema:

{{
  "lmic_region": "Sub-Saharan Africa or not reported",
  "health_domain": "",
  "study_design": "",
  "setting": "national | district | hospital | primary care | community | mixed | not reported",
  "intervention_description": "",
  "implementation_outcome_focus": "",
  "barriers": [],
  "enablers": [],
  "outcomes_measured": [],
  "funding_reported": "yes | no | unclear | not reported",
  "funding_level_estimate": "none | low | moderate | high | unclear | not reported",
  "kt_strategy_mentioned": "",
  "is_real_implementation_project": true,
  "reason_for_inclusion": "",
  "extraction_confidence": "high | medium | low"
}}

Title:
{title}

Abstract:
{abstract}
"""

    return prompt.strip()


def complete_record(article, llm_record):
    """
    Combine trusted article metadata with Gemini extraction.

    Metadata such as PMID, title, year, journal, and country should come
    from our PubMed/article data, not from the LLM.
    """
    today = date.today().isoformat()

    pmid = article.get("pmid", "not reported")
    title = article.get("title", "not reported")
    year = article.get("year", "not reported")
    journal = article.get("journal", "not reported")
    country = article.get("country", "Ethiopia")

    final_record = {
        "record_id": f"PMID-{pmid}",
        "pmid": pmid,
        "title": title,
        "year": year,
        "journal": journal,
        "country": country,
        "lmic_region": "not reported",
        "health_domain": "not reported",
        "study_design": "not reported",
        "setting": "not reported",
        "intervention_description": "not reported",
        "implementation_outcome_focus": "not reported",
        "barriers": [],
        "enablers": [],
        "outcomes_measured": [],
        "funding_reported": "not reported",
        "funding_level_estimate": "not reported",
        "kt_strategy_mentioned": "not reported",
        "is_real_implementation_project": True,
        "reason_for_inclusion": "not reported",
        "extraction_confidence": "low",
        "abstract_source": True,
        "extraction_date": today,
        "human_validation_status": "pending",
    }

    if llm_record:
        for key, value in llm_record.items():
            if key in final_record:
                final_record[key] = value

    # Force trusted metadata again after merging LLM output.
    final_record["record_id"] = f"PMID-{pmid}"
    final_record["pmid"] = pmid
    final_record["title"] = title
    final_record["year"] = year
    final_record["journal"] = journal
    final_record["country"] = country
    final_record["abstract_source"] = True
    final_record["human_validation_status"] = "pending"
    final_record["extraction_date"] = today

    return final_record


def extract_record_with_gemini(article):
    """
    Send one article to Gemini and return a complete structured record.
    """
    client = get_gemini_client()
    prompt = build_extraction_prompt(article)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    llm_record = clean_llm_json(response.text)

    if llm_record is None:
        return None

    return complete_record(article, llm_record)


def load_first_raw_article(path=RAW_ARTICLES_PATH):
    """
    Load the first article from our raw PubMed JSONL file.
    JSONL means: one JSON object per line.
    """
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

            if "country" not in article:
                article["country"] = "Ethiopia"

            return article

    raise ValueError(f"No articles found in {path}.")


def demo_article():
    """
    A fake/simple article for testing Gemini extraction.
    Kept as fallback, but Day 18 uses a real saved PubMed article.
    """
    return {
        "pmid": "12345678",
        "title": "Implementation of a primary health care quality improvement program in Ethiopia",
        "abstract": (
            "This study describes the implementation of a quality improvement "
            "program in primary health care facilities in Ethiopia. The intervention "
            "included provider training, audit and feedback, supportive supervision, "
            "and use of local implementation teams. Reported barriers included "
            "limited staffing, supply shortages, and competing clinical priorities. "
            "Facilitators included leadership support, regular mentorship, and "
            "community engagement. Outcomes included service readiness, adherence "
            "to clinical guidelines, and provider-reported feasibility."
        ),
        "year": "2023",
        "journal": "Implementation Science Communications",
        "country": "Ethiopia",
    }


if __name__ == "__main__":
    article = load_first_raw_article()
    record = extract_record_with_gemini(article)

    if record is None:
        print("Gemini extraction failed.")
    else:
        print("\nGemini real PubMed article test")
        print("=" * 40)
        print(f"PMID: {record['pmid']}")
        print(f"Title: {record['title']}")
        print(f"Is real implementation project? {record['is_real_implementation_project']}")
        print(f"Reason: {record['reason_for_inclusion']}")
        print("\nFull structured record:")
        print(json.dumps(record, indent=2, ensure_ascii=False))
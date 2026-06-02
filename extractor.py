import json
import re
from pathlib import Path

from database import load_records, save_record


INPUT_FILE = "data/screened_articles.jsonl"
OUTPUT_FILE = "data/extracted_records.jsonl"


IMPLEMENTATION_TERMS = [
    "implementation",
    "implemented",
    "implementing",
    "knowledge translation",
    "implementation science",
    "adoption",
    "uptake",
    "scale-up",
    "rollout",
    "quality improvement",
    "guideline",
    "checklist",
    "intervention",
]


BARRIER_TERMS = [
    "barrier",
    "barriers",
    "challenge",
    "challenges",
    "lack",
    "limited",
    "shortage",
    "constraint",
    "underfunded",
    "fragile",
    "disrepair",
    "poor",
    "weakness",
    "resource limitations",
]


FACILITATOR_TERMS = [
    "support",
    "supportive",
    "leadership",
    "training",
    "guideline",
    "checklist",
    "standardized",
    "readiness",
    "policy",
    "recommendations",
    "education",
    "counseling",
    "infrastructure",
]


def find_matching_terms(text, terms):
    text_lower = text.lower()
    matches = []

    for term in terms:
        if term.lower() in text_lower:
            matches.append(term)

    return matches


def split_sentences(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def find_relevant_sentences(text, terms, max_sentences=3):
    sentences = split_sentences(text)
    selected_sentences = []

    for sentence in sentences:
        sentence_lower = sentence.lower()

        for term in terms:
            if term.lower() in sentence_lower:
                selected_sentences.append(sentence.strip())
                break

        if len(selected_sentences) >= max_sentences:
            break

    return selected_sentences


def detect_study_design(text):
    text_lower = text.lower()

    if "systematic review" in text_lower:
        return "systematic_review"

    if "randomized" in text_lower or "randomised" in text_lower:
        return "randomized_trial"

    if "cross-sectional" in text_lower or "cross sectional" in text_lower:
        return "cross_sectional"

    if "prospective observational" in text_lower:
        return "prospective_observational"

    if "observational" in text_lower:
        return "observational"

    if "qualitative" in text_lower:
        return "qualitative"

    if "mixed methods" in text_lower:
        return "mixed_methods"

    if "before-after" in text_lower or "before and after" in text_lower:
        return "before_after"

    if "cohort" in text_lower:
        return "cohort"

    if "viewpoint" in text_lower or "commentary" in text_lower:
        return "viewpoint"

    return "unclear"


def extract_record(article):
    title = article.get("title", "")
    abstract = article.get("abstract", "")
    text = f"{title} {abstract}"

    extracted_record = {
        "pmid": article.get("pmid", "").strip(),
        "title": title,
        "country": article.get("country", ""),
        "source": article.get("source", ""),
        "screening_decision": article.get("screening_decision", ""),
        "study_design": detect_study_design(text),
        "implementation_signals": find_matching_terms(text, IMPLEMENTATION_TERMS),
        "barriers": find_relevant_sentences(text, BARRIER_TERMS),
        "facilitators": find_relevant_sentences(text, FACILITATOR_TERMS),
        "extraction_method": "rule_based_v1",
        "needs_human_review": True,
    }

    return extracted_record


def extract_records():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    if output_path.exists():
        output_path.unlink()

    screened_articles = load_records(INPUT_FILE)
    extracted_records = []
    skipped_count = 0

    for article in screened_articles:
        if article.get("screening_decision") != "include":
            skipped_count += 1
            continue

        extracted_record = extract_record(article)
        extracted_records.append(extracted_record)
        save_record(extracted_record, OUTPUT_FILE)

    return extracted_records, skipped_count


if __name__ == "__main__":
    extracted_records, skipped_count = extract_records()

    print(f"Extracted {len(extracted_records)} records")
    print(f"Skipped {skipped_count} excluded articles")
    print(f"Saved results to {OUTPUT_FILE}")

    for record in extracted_records:
        print("-" * 40)
        print("PMID:", record["pmid"])
        print("Title:", record["title"])
        print("Study design:", record["study_design"])
        print("Implementation signals:", record["implementation_signals"])
        print("Barriers found:", len(record["barriers"]))
        print("Facilitators found:", len(record["facilitators"]))

    if extracted_records:
        print("-" * 40)
        print("First extracted record:")
        print(json.dumps(extracted_records[0], indent=2))
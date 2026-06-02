from pathlib import Path

from database import load_records, save_record


INPUT_FILE = "data/raw_pubmed_articles.jsonl"
OUTPUT_FILE = "data/screened_articles.jsonl"


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
    "barrier",
    "facilitator",
    "quality improvement",
    "guideline",
    "checklist",
    "intervention",
]


HEALTH_TERMS = [
    "health",
    "hospital",
    "clinical",
    "patient",
    "patients",
    "disease",
    "maternal",
    "surgical",
    "anxiety",
    "delivery",
    "care",
    "healthcare",
    "health system",
]


REAL_WORLD_TERMS = [
    "hospital",
    "clinic",
    "health center",
    "facility",
    "community",
    "patients",
    "women",
    "health system",
    "program",
    "service",
    "care",
]


EXCLUSION_TERMS = [
    "stove",
    "biogas",
    "injera",
    "crop",
    "livestock",
    "soil",
    "agriculture",
]


def contains_any(text, terms):
    text = text.lower()

    for term in terms:
        if term in text:
            return True

    return False


def screen_article(article):
    title = article.get("title", "")
    abstract = article.get("abstract", "")

    text = f"{title} {abstract}"

    has_implementation = contains_any(text, IMPLEMENTATION_TERMS)
    has_health = contains_any(text, HEALTH_TERMS)
    has_real_world = contains_any(text, REAL_WORLD_TERMS)
    has_exclusion = contains_any(text, EXCLUSION_TERMS)

    reasons = []

    if has_implementation:
        reasons.append("Contains implementation-related terms")

    if has_health:
        reasons.append("Contains health-related terms")

    if has_real_world:
        reasons.append("Contains real-world setting terms")

    if has_exclusion:
        reasons.append("Contains likely exclusion terms")

    if has_exclusion:
        decision = "exclude"
    elif has_implementation and has_health and has_real_world:
        decision = "include"
    else:
        decision = "exclude"

    screened_article = article.copy()
    screened_article["screening_decision"] = decision
    screened_article["screening_reasons"] = reasons

    return screened_article


def screen_articles():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    if output_path.exists():
        output_path.unlink()

    articles = load_records(INPUT_FILE)
    screened_articles = []

    for article in articles:
        screened_article = screen_article(article)
        screened_articles.append(screened_article)
        save_record(screened_article, OUTPUT_FILE)

    return screened_articles


if __name__ == "__main__":
    screened_articles = screen_articles()

    include_count = 0
    exclude_count = 0

    for article in screened_articles:
        if article["screening_decision"] == "include":
            include_count += 1
        else:
            exclude_count += 1

    print(f"Screened {len(screened_articles)} articles")
    print(f"Included: {include_count}")
    print(f"Excluded: {exclude_count}")
    print(f"Saved results to {OUTPUT_FILE}")

    for article in screened_articles:
        print("-" * 40)
        print("PMID:", article["pmid"])
        print("Decision:", article["screening_decision"])
        print("Title:", article["title"])
        print("Reasons:", article["screening_reasons"])
from collect_pubmed import collect_pubmed_articles
from extractor import extract_records
from profiler import create_country_profile
from screener import screen_articles


def print_step(step_number, message):
    print("")
    print("=" * 60)
    print(f"STEP {step_number}: {message}")
    print("=" * 60)


def run_pipeline():
    print_step(1, "Collect raw PubMed articles")
    raw_articles = collect_pubmed_articles()
    print(f"Collected raw articles: {len(raw_articles)}")

    print_step(2, "Screen articles")
    screened_articles = screen_articles()

    include_count = 0
    exclude_count = 0

    for article in screened_articles:
        if article["screening_decision"] == "include":
            include_count += 1
        else:
            exclude_count += 1

    print(f"Screened articles: {len(screened_articles)}")
    print(f"Included: {include_count}")
    print(f"Excluded: {exclude_count}")

    print_step(3, "Extract structured records")
    extracted_records, skipped_count = extract_records()
    print(f"Extracted records: {len(extracted_records)}")
    print(f"Skipped excluded articles: {skipped_count}")

    print_step(4, "Generate country profile")
    create_country_profile()
    print("Generated profile: outputs/ethiopia_profile.md")

    print_step(5, "Pipeline complete")
    print("Raw articles: data/raw_pubmed_articles.jsonl")
    print("Screened articles: data/screened_articles.jsonl")
    print("Extracted records: data/extracted_records.jsonl")
    print("Country profile: outputs/ethiopia_profile.md")


if __name__ == "__main__":
    run_pipeline()
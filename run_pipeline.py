from agent_decision import decide_next_step, summarize_screening
from collect_pubmed import COUNTRY, MAX_RESULTS, QUERY, collect_pubmed_articles
from extractor import extract_records
from profiler import create_country_profile
from screener import screen_articles


BROAD_QUERY = (
    '(implementation OR implemented OR implementing OR '
    '"knowledge translation" OR "implementation science" OR '
    'adoption OR uptake OR checklist OR guideline) AND Ethiopia'
)


def print_step(step_number, message):
    print("")
    print("=" * 60)
    print(f"STEP {step_number}: {message}")
    print("=" * 60)


def print_screening_summary(screening_summary):
    print(f"Screened articles: {screening_summary['total']}")
    print(f"Included: {screening_summary['included']}")
    print(f"Excluded: {screening_summary['excluded']}")


def run_pipeline():
    print_step(1, "Collect raw PubMed articles")
    raw_articles = collect_pubmed_articles(
        query=QUERY,
        country=COUNTRY,
        max_results=MAX_RESULTS,
    )
    print(f"Collected raw articles: {len(raw_articles)}")

    print_step(2, "Screen articles")
    screened_articles = screen_articles()
    screening_summary = summarize_screening(screened_articles)
    print_screening_summary(screening_summary)

    print_step(3, "Agentic decision")
    decision = decide_next_step(screening_summary)
    print("Decision:", decision["action"])
    print("Reason:", decision["reason"])

    if decision["action"] == "broaden_search":
        print("Running broader PubMed search...")

        raw_articles = collect_pubmed_articles(
            query=BROAD_QUERY,
            country=COUNTRY,
            max_results=MAX_RESULTS,
        )

        print(f"Collected raw articles after broader search: {len(raw_articles)}")

        screened_articles = screen_articles()
        screening_summary = summarize_screening(screened_articles)
        print_screening_summary(screening_summary)

    print_step(4, "Extract structured records")
    extracted_records, skipped_count = extract_records()
    print(f"Extracted records: {len(extracted_records)}")
    print(f"Skipped excluded articles: {skipped_count}")

    print_step(5, "Generate country profile")
    create_country_profile()
    print("Generated profile: outputs/ethiopia_profile.md")

    print_step(6, "Pipeline complete")
    print("Raw articles: data/raw_pubmed_articles.jsonl")
    print("Screened articles: data/screened_articles.jsonl")
    print("Extracted records: data/extracted_records.jsonl")
    print("Country profile: outputs/ethiopia_profile.md")


if __name__ == "__main__":
    run_pipeline()
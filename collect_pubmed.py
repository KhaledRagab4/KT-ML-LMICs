from pathlib import Path

from database import save_record
from pubmed_tool import fetch_article_details, search_pubmed


OUTPUT_FILE = "data/raw_pubmed_articles.jsonl"

COUNTRY = "Ethiopia"

QUERY = '(implementation[Title/Abstract] OR implemented[Title/Abstract] OR "knowledge translation"[Title/Abstract] OR "implementation science"[Title/Abstract]) AND Ethiopia[Title/Abstract]'

MAX_RESULTS = 5


def collect_pubmed_articles(
    query=QUERY,
    country=COUNTRY,
    max_results=MAX_RESULTS,
    output_file=OUTPUT_FILE,
):
    output_path = Path(output_file)

    if output_path.exists():
        output_path.unlink()

    pmids = search_pubmed(query, max_results=max_results)
    articles = fetch_article_details(pmids)

    for article in articles:
        article["country"] = country
        article["source"] = "PubMed"
        article["query"] = query

        save_record(article, output_file)

    return articles


if __name__ == "__main__":
    articles = collect_pubmed_articles()

    print(f"Saved {len(articles)} articles to {OUTPUT_FILE}")

    for article in articles:
        print("-" * 40)
        print("PMID:", article["pmid"])
        print("Title:", article["title"])
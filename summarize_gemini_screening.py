import json
import os
from collections import Counter


SCREENED_PATH = "data/gemini_screened_articles.jsonl"
OUTPUT_PATH = "outputs/gemini_screening_summary.md"


def load_jsonl(path):
    """
    Load a JSONL file.
    JSONL means one JSON object per line.
    """
    records = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find {path}")

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            records.append(json.loads(line))

    return records


def summarize_records(records):
    """
    Count Gemini screening decisions, exclusion categories, and confidence levels.
    """
    decisions = Counter()
    exclusion_categories = Counter()
    confidence_levels = Counter()

    for record in records:
        screening = record.get("gemini_screening") or {}

        decision = screening.get("decision", "missing")
        exclusion_category = screening.get("exclusion_category", "missing")
        confidence = screening.get("confidence", "missing")

        decisions[decision] += 1
        exclusion_categories[exclusion_category] += 1
        confidence_levels[confidence] += 1

    return {
        "total_records": len(records),
        "decisions": decisions,
        "exclusion_categories": exclusion_categories,
        "confidence_levels": confidence_levels,
    }


def counter_to_markdown(counter):
    """
    Convert a Counter object into markdown bullet points.
    """
    if not counter:
        return "- None\n"

    lines = []

    for key, count in counter.items():
        lines.append(f"- {key}: {count}")

    return "\n".join(lines) + "\n"


def build_markdown_report(records, summary):
    """
    Build a markdown report from Gemini screening results.
    """
    lines = []

    lines.append("# Gemini Screening Summary")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append(
        "This file summarizes a Gemini-based screening test on the first "
        "five raw PubMed records collected by the project."
    )
    lines.append("")
    lines.append(
        "The goal is to test whether an LLM can identify likely false positives "
        "from the initial rule-based PubMed screening pipeline."
    )
    lines.append("")

    lines.append("## Summary counts")
    lines.append("")
    lines.append(f"- Total records screened: {summary['total_records']}")
    lines.append("")

    lines.append("### Decisions")
    lines.append("")
    lines.append(counter_to_markdown(summary["decisions"]))

    lines.append("### Exclusion categories")
    lines.append("")
    lines.append(counter_to_markdown(summary["exclusion_categories"]))

    lines.append("### Confidence levels")
    lines.append("")
    lines.append(counter_to_markdown(summary["confidence_levels"]))

    lines.append("## Article-level decisions")
    lines.append("")

    for index, record in enumerate(records, start=1):
        screening = record.get("gemini_screening") or {}

        pmid = record.get("pmid", "not reported")
        title = record.get("title", "not reported")
        decision = screening.get("decision", "missing")
        reason = screening.get("reason", "missing")
        exclusion_category = screening.get("exclusion_category", "missing")
        confidence = screening.get("confidence", "missing")

        lines.append(f"### Article {index}")
        lines.append("")
        lines.append(f"- PMID: {pmid}")
        lines.append(f"- Title: {title}")
        lines.append(f"- Decision: {decision}")
        lines.append(f"- Exclusion category: {exclusion_category}")
        lines.append(f"- Confidence: {confidence}")
        lines.append(f"- Reason: {reason}")
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "In this batch, Gemini classified all five records as excluded. "
        "This suggests that the initial rule-based screening pipeline may be "
        "too broad and may include epidemiological, clinical observational, "
        "editorial/framework, or non-health implementation records."
    )
    lines.append("")
    lines.append(
        "This supports adding an LLM-assisted screening step before structured "
        "evidence extraction."
    )
    lines.append("")

    lines.append("## Limitations")
    lines.append("")
    lines.append("- This is a small test batch of only five PubMed records.")
    lines.append("- Screening is based on abstracts only.")
    lines.append("- Gemini decisions require human validation before research use.")
    lines.append("- This is a prototype, not a systematic-review-grade screening process.")
    lines.append("")

    return "\n".join(lines)


def save_markdown_report(markdown_text, path=OUTPUT_PATH):
    """
    Save markdown text to a file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(markdown_text)


def main():
    """
    Load Gemini screening results, summarize them, and save a markdown report.
    """
    records = load_jsonl(SCREENED_PATH)
    summary = summarize_records(records)
    markdown_report = build_markdown_report(records, summary)

    save_markdown_report(markdown_report)

    print("Gemini screening summary generated.")
    print(f"Input: {SCREENED_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Records summarized: {summary['total_records']}")


if __name__ == "__main__":
    main()
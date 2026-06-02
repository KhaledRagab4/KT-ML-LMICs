from collections import Counter
from pathlib import Path

from database import load_records


INPUT_FILE = "data/extracted_records.jsonl"
OUTPUT_FILE = "outputs/ethiopia_profile.md"
COUNTRY = "Ethiopia"


def count_list_values(records, field_name):
    counter = Counter()

    for record in records:
        values = record.get(field_name, [])

        for value in values:
            counter[value] += 1

    return counter


def format_counter_section(title, counter, max_items=10):
    lines = [
        f"## {title}",
        "",
    ]

    if not counter:
        lines.append("No items found.")
        lines.append("")
        return lines

    for item, count in counter.most_common(max_items):
        lines.append(f"- {item} ({count})")

    lines.append("")
    return lines


def build_country_profile(records, country):
    country_records = []

    for record in records:
        record_country = record.get("country", "")

        if record_country.lower() == country.lower():
            country_records.append(record)

    study_design_counter = Counter(
        record.get("study_design") or "unclear"
        for record in country_records
    )

    implementation_signal_counter = count_list_values(
        country_records,
        "implementation_signals",
    )

    barrier_counter = count_list_values(
        country_records,
        "barriers",
    )

    facilitator_counter = count_list_values(
        country_records,
        "facilitators",
    )

    lines = [
        f"# {country} Implementation Evidence Profile",
        "",
        "## Summary",
        "",
        f"- Country: {country}",
        f"- Total extracted records: {len(country_records)}",
        "",
    ]

    lines.extend(
        format_counter_section(
            "Study designs",
            study_design_counter,
        )
    )

    lines.extend(
        format_counter_section(
            "Implementation signals",
            implementation_signal_counter,
        )
    )

    lines.extend(
        format_counter_section(
            "Potential barriers",
            barrier_counter,
            max_items=5,
        )
    )

    lines.extend(
        format_counter_section(
            "Potential facilitators",
            facilitator_counter,
            max_items=5,
        )
    )

    lines.extend([
        "## Included articles",
        "",
    ])

    if not country_records:
        lines.append("No extracted records found for this country.")
        lines.append("")
    else:
        for record in country_records:
            pmid = record.get("pmid", "").strip()
            title = record.get("title", "").strip()
            study_design = record.get("study_design", "unclear")

            lines.append(
                f"- PMID {pmid}: {title} "
                f"[study design: {study_design}]"
            )

        lines.append("")

    return "\n".join(lines)


def save_profile(profile_text, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(profile_text, encoding="utf-8")


def create_country_profile():
    input_path = Path(INPUT_FILE)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    records = load_records(INPUT_FILE)

    profile_text = build_country_profile(
        records,
        COUNTRY,
    )

    save_profile(
        profile_text,
        OUTPUT_FILE,
    )

    return profile_text


if __name__ == "__main__":
    profile = create_country_profile()

    print(profile)
    print(f"Saved profile to {OUTPUT_FILE}")
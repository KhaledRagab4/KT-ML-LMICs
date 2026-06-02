MIN_INCLUDED_ARTICLES = 4


def summarize_screening(screened_articles):
    include_count = 0
    exclude_count = 0

    for article in screened_articles:
        if article["screening_decision"] == "include":
            include_count += 1
        else:
            exclude_count += 1

    return {
        "total": len(screened_articles),
        "included": include_count,
        "excluded": exclude_count,
    }


def decide_next_step(screening_summary):
    included = screening_summary["included"]

    if included < MIN_INCLUDED_ARTICLES:
        return {
            "action": "broaden_search",
            "reason": (
                f"Only {included} included articles found. "
                f"Minimum required is {MIN_INCLUDED_ARTICLES}."
            ),
        }

    return {
        "action": "continue_pipeline",
        "reason": (
            f"Found {included} included articles. "
            f"This meets the minimum requirement of {MIN_INCLUDED_ARTICLES}."
        ),
    }
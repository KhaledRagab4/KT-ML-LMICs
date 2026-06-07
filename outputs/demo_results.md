# Demo Results

## Project

**Published LMIC Implementation Evidence Agent**

This demo shows the current working state of the `KT-ML-LMICs` prototype.

The project currently has two layers:

1. A rule-based PubMed pipeline.
2. Independent Gemini-based screening and extraction tests.

## Rule-based pipeline demo

Command:

```powershell
python run_pipeline.py
```

Main outputs:

```text
data/raw_pubmed_articles.jsonl
data/screened_articles.jsonl
data/extracted_records.jsonl
outputs/ethiopia_profile.md
```

## Gemini screening demo

Command:

```powershell
python gemini_screener.py
```

Result:

```text
Included: 0
Excluded: 5
Uncertain: 0
```

Gemini outputs:

```text
data/gemini_screened_articles.jsonl
outputs/gemini_screening_summary.md
```

## Key observation

The original rule-based pipeline is useful as a first prototype, but the Gemini screening test suggests that the initial rule-based screening is too broad.

Gemini excluded all five tested records because they were not clear implementation or knowledge translation evidence.

## Current limitations

- PubMed does not index all implementation projects.
- This project currently uses abstracts only.
- The current pilot focuses on Ethiopia only.
- Gemini screening and extraction may still misclassify studies.
- Human validation is required before research use.
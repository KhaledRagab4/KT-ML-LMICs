# KT-ML-LMICs

## Project title

**Published LMIC Implementation Evidence Agent**

A beginner-friendly Python prototype that searches PubMed for published implementation and knowledge translation evidence from LMIC contexts, screens candidate articles, extracts structured records, applies a simple agentic decision point, and generates country-level evidence profiles.

## What does the name mean?

KT-ML-LMICs stands for:

- **KT**: Knowledge Translation
- **ML**: Machine Learning
- **LMICs**: Low- and Middle-Income Countries

## Current MVP

The current pilot country is:

- Ethiopia

The project currently supports:

- PubMed search using NCBI E-utilities
- Fetching PubMed titles and abstracts
- Saving raw PubMed records as JSONL
- Rule-based article screening
- A simple agentic decision point
- Rule-based structured extraction
- Markdown country profile generation
- Gemini API connection testing
- Gemini structured extraction testing
- Gemini screening of real PubMed records
- Saving Gemini screening decisions to JSONL
- Generating a Gemini screening summary report

## Why this project exists

This project is not trying to build a complete systematic review tool.

It is a practical learning MVP for combining:

- Python
- PubMed APIs
- JSONL evidence storage
- basic screening logic
- LLM-assisted screening and extraction
- simple agentic decision-making
- research-oriented documentation

The long-term goal is to support Knowledge Translation, Implementation Science, Global Health, and LMIC health systems research.

## Important methodological note

This prototype does **not** claim to capture all LMIC implementation projects.

A more accurate description is:

> This prototype captures published PubMed-indexed implementation evidence from selected LMIC contexts, extracted from abstracts only.

Current extraction and screening outputs require human validation before research use.

## How to set up

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create a local `.env` file based on `.env.example`:

```text
OPENAI_API_KEY=
GEMINI_API_KEY=
```

For the current Gemini workflow, `GEMINI_API_KEY` is required.

## How to run the original rule-based pipeline

```powershell
python run_pipeline.py
```

Expected outputs:

```text
data/raw_pubmed_articles.jsonl
data/screened_articles.jsonl
data/extracted_records.jsonl
outputs/ethiopia_profile.md
```

## How to run Gemini tests

Test Gemini structured extraction:

```powershell
python gemini_extractor.py
```

Run Gemini screening on the first five raw PubMed records:

```powershell
python gemini_screener.py
```

Summarize Gemini screening results:

```powershell
python summarize_gemini_screening.py
```

Gemini outputs:

```text
data/gemini_screened_articles.jsonl
outputs/gemini_screening_summary.md
```

## Current Gemini screening result

In the first Gemini screening batch, Gemini excluded all five tested PubMed records:

```text
Included: 0
Excluded: 5
Uncertain: 0
```

This suggests that the initial rule-based PubMed screening is broad and may include false positives such as:

- epidemiological studies
- clinical observational studies
- editorial or framework articles
- non-health implementation records

This is useful because it shows why an LLM-assisted screening step can improve the pipeline before structured extraction.

## Main files

```text
pubmed_tool.py                  PubMed search and fetch functions
collect_pubmed.py               Collects raw PubMed articles
database.py                     JSONL save/load helpers
screener.py                     Rule-based article screening
agent_decision.py               Simple agentic decision point
extractor.py                    Rule-based structured extraction
profiler.py                     Generates the country evidence profile
run_pipeline.py                 Runs the full rule-based workflow

llm_extractor.py                OpenAI API scaffold; currently limited by API quota
gemini_extractor.py             Gemini connection and structured extraction tests
gemini_screener.py              Gemini screening batch test
summarize_gemini_screening.py   Generates Gemini screening summary report
```

## Main outputs

```text
data/raw_pubmed_articles.jsonl
data/screened_articles.jsonl
data/extracted_records.jsonl
data/gemini_screened_articles.jsonl

outputs/ethiopia_profile.md
outputs/gemini_screening_summary.md
```

## Limitations

- PubMed does not index all implementation projects.
- This project currently uses abstracts only.
- Rule-based screening is broad and may include false positives.
- Gemini screening and extraction may still misclassify studies.
- Human validation is required before research use.
- The current search strategy is pilot-level, not systematic-review-grade.
- The current pilot focuses on Ethiopia only.

## Current status

The project now has two layers:

1. A working rule-based PubMed pipeline.
2. Independent Gemini screening and extraction tests.

The next development step is to integrate Gemini screening into the pipeline carefully, without breaking the working rule-based version.
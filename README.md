# KT-ML-LMICs

## What does the name mean?

KT-ML-LMICs stands for:

- **KT**: Knowledge Translation
- **ML**: Machine Learning
- **LMICs**: Low- and Middle-Income Countries

This project is a learning MVP that uses Python, PubMed APIs, rule-based screening, and later LLM-assisted extraction to organize implementation and knowledge translation evidence from LMICs.

## Project title

**Published LMIC Implementation Evidence Agent**

A Python prototype that searches PubMed for implementation and knowledge translation evidence in LMICs, screens candidate articles, extracts structured records, applies a simple agentic decision point, and generates a simple country evidence profile.

## Current MVP

The pipeline currently supports Ethiopia as the pilot country.

It can:

- Search PubMed using NCBI E-utilities
- Fetch article titles and abstracts
- Save raw PubMed records as JSONL
- Screen candidate articles using rule-based logic
- Apply a simple agentic decision point
- Extract structured implementation evidence fields
- Generate a Markdown country profile

## Project pipeline

```text
Search PubMed
->
Fetch abstracts
->
Save raw articles
->
Screen articles
->
Agentic decision
->
Extract structured records
->
Generate country profile

How to run

Activate the virtual environment first:

.venv\Scripts\activate

Run the full pipeline:

python run_pipeline.py
Main outputs
data/raw_pubmed_articles.jsonl
data/screened_articles.jsonl
data/extracted_records.jsonl
outputs/ethiopia_profile.md
Main files
pubmed_tool.py       PubMed search and fetch functions
collect_pubmed.py    Collects raw PubMed articles
screener.py          Rule-based article screening
agent_decision.py    Simple agentic decision point
extractor.py         Rule-based structured extraction
profiler.py          Generates the country evidence profile
run_pipeline.py      Runs the full workflow
database.py          JSONL save/load helpers
Important note

This is a learning MVP. Screening and extraction are currently rule-based and should be reviewed by a human. LLM-based structured extraction can be added later.
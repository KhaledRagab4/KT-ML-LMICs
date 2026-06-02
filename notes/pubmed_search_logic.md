# PubMed Search Logic

## Goal

The goal of this step is to search PubMed and get a list of PubMed IDs (PMIDs).

Later, each PMID will be used to fetch article details such as title and abstract.

---

## What is PubMed?

PubMed is a database for biomedical literature.

In this project, we use PubMed to find papers about implementation and knowledge translation evidence in LMICs.

---

## What is an API?

An API is a way for one program to ask another system for data.

Instead of opening PubMed manually in the browser, our Python code will send a request to PubMed and receive results.

---

## What is NCBI E-utilities?

NCBI E-utilities are tools that allow software to search and retrieve data from NCBI databases.

For this project, we will use ESearch first.

---

## What is ESearch?

ESearch searches a database using a text query.

For PubMed, ESearch can return a list of PubMed IDs matching our search.

---

## What is a PMID?

PMID means PubMed ID.

It is a unique identifier for one PubMed article.

Example:

12345678

---

## ESearch URL structure

Base URL:

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi

Important parameters:

db=pubmed
term=implementation Ethiopia
retmode=json
retmax=5

---

## Example full URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=implementation%20Ethiopia&retmode=json&retmax=5

---

## What this URL means

db=pubmed means search inside PubMed.

term=implementation Ethiopia means search for articles matching these words.

retmode=json means return the result as JSON.

retmax=5 means return only 5 IDs for now.

---

## Why we start with PMIDs only

Searching returns IDs first.

Fetching title and abstract is a separate step.

This keeps the project simple and easier to debug.

---

## Why use requests instead of Biopython?

requests teaches the API logic directly.

Biopython can hide some details, but our goal is to understand tool use and API calls clearly.

---

## Project flow

Search PubMed
->
Get PMIDs
->
Fetch article details
->
Screen implementation evidence
->
Extract structured JSON
->
Save to JSONL
->
Generate country profile

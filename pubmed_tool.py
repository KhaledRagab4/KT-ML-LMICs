import requests
import xml.etree.ElementTree as ET


SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def search_pubmed(query, max_results=5):
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }

    response = requests.get(SEARCH_URL, params=params)
    response.raise_for_status()

    data = response.json()
    pmids = data["esearchresult"]["idlist"]

    return pmids


def fetch_article_details(pmids):
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }

    response = requests.get(FETCH_URL, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)

    articles = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        abstract_parts = article.findall(".//AbstractText")

        abstract = " ".join(
            part.text for part in abstract_parts if part.text
        )

        articles.append({
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
        })

    return articles


if __name__ == "__main__":
    query = "implementation Ethiopia"
    pmids = search_pubmed(query, max_results=3)
    articles = fetch_article_details(pmids)

    print("Query:", query)
    print("PMIDs:", pmids)

    for article in articles:
        print("-" * 40)
        print("PMID:", article["pmid"])
        print("Title:", article["title"])
        print("Abstract:", article["abstract"][:500])
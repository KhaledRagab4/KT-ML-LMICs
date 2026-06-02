import requests


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def search_pubmed(query, max_results=5):
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()
    pmids = data["esearchresult"]["idlist"]

    return pmids


if __name__ == "__main__":
    query = "implementation Ethiopia"
    pmids = search_pubmed(query, max_results=5)

    print("Query:", query)
    print("PMIDs:", pmids)
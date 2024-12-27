import os
import time
import requests
import warnings
import numpy as np
import pandas as pd

from typing import Optional, Any
from pandas.core.frame import DataFrame

from retry import retry


def _sleep1() -> None:
    # semantic scholar api is restricted under 1 qps
    # so we sleep 1 second anyway to avoid rate limit
    time.sleep(1)


def _get_headers() -> dict[str, str]:
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

    if api_key is None:
        warnings.warn(
            "You have not set semantic scholar api key using environment `SEMANTIC_SCHOLAR_API_KEY`, "
            "this may fall back to use the public usage of semantic scholar api."
        )
        headers = None
    else:
        headers = {"x-api-key": api_key}

    return headers


def _get_details(paper_ids: list[str], fields: list[str]) -> dict[str, Any]:
    _sleep1()

    headers = _get_headers()
    url = "https://api.semanticscholar.org/graph/v1/paper/batch"

    rsp = requests.post(
        url,
        headers=headers,
        json={"ids": paper_ids},
        params={"fields": ",".join(fields)},
        timeout=300,
    )
    rsp.raise_for_status()

    return rsp.json()


@retry(tries=3)
def get_paper_id_from_title(title: str) -> Optional[str]:
    _sleep1()

    headers = _get_headers()
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query=title:{title}&limit=1"

    rsp = requests.get(url, headers=headers, timeout=300)
    rsp.raise_for_status()

    data = rsp.json().get("data", None)
    # not data available
    if data is None or len(data) == 0:
        return None

    if data[0]["title"].lower() == title.lower():
        return data[0]["paperId"]
    else:
        # retrieved title does not match with the query
        return None


@retry(tries=3)
def get_paper_id_from_arxiv(arxiv_id: str) -> Optional[str]:
    _sleep1()

    headers = _get_headers()
    url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}"

    rsp = requests.get(url, headers=headers, timeout=300)
    rsp.raise_for_status()

    paper_id = rsp.json().get("paperId", None)
    return paper_id


def get_paper_id(paper: str) -> Optional[str]:
    try:
        title_paper_id = get_paper_id_from_title(paper)
    except Exception:
        title_paper_id = None

    try:
        arxiv_paper_id = get_paper_id_from_arxiv(paper)
    except Exception:
        arxiv_paper_id = None

    return title_paper_id if title_paper_id is not None else arxiv_paper_id


@retry(tries=3)
def get_references(paper_id: str) -> list[str]:
    fields = ["references"]
    details = _get_details([paper_id], fields)

    references = details[0]["references"]
    paper_ids = [ref["paperId"] for ref in references if ref["paperId"] is not None]

    return paper_ids


@retry(tries=3)
def get_paper_details(paper_ids: list[str]) -> DataFrame:
    fields = [
        "paperId",
        "externalIds",
        "title",
        "abstract",
        "tldr",
        "publicationDate",
        "referenceCount",
        "citationCount",
        "openAccessPdf",
    ]
    details = _get_details(paper_ids, fields)

    df = pd.DataFrame.from_dict(details)
    df = df.rename(
        columns={
            "paperId": "paper_id",
            "referenceCount": "reference_count",
            "citationCount": "citation_count",
            "openAccessPdf": "pdf",
            "publicationDate": "publication_date",
            "tldr": "summary",
        }
    )

    # stanardrize all fields
    df["arxiv_id"] = df["externalIds"].apply(lambda x: x.get("ArXiv", None) if not pd.isna(x) else x)
    df["summary"] = df["summary"].apply(lambda x: x["text"] if not pd.isna(x) else x)
    df["pdf"] = df["pdf"].apply(lambda x: x["url"] if not pd.isna(x) else x)
    df["publication_date"] = pd.to_datetime(df["publication_date"])
    # try to infer the pdf if pdf is not available but arxiv_id is
    condition = (~df["arxiv_id"].isna()) & (df["pdf"].isna())
    df.loc[condition, "pdf"] = df[condition]["arxiv_id"].apply(lambda x: f"https://arxiv.org/pdf/{x}")
    df = df[
        [
            "paper_id",
            "arxiv_id",
            "title",
            "abstract",
            "summary",
            "publication_date",
            "reference_count",
            "citation_count",
            "pdf",
        ]
    ]

    df = df.replace({np.nan: None})

    return df

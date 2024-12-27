from typing import Optional, Any
from pandas.core.frame import DataFrame

from neomodel import db
from neomodel.integration.pandas import to_dataframe


class SafeExecutionException(Exception):
    def __init__(self, *args):
        message = "Cannot execute modify cypher query in safe mode."
        super().__init__(message, *args)


@db.transaction
def execute_cypher_query(query: str, params: Optional[dict[str, Any]] = None) -> DataFrame:
    df = to_dataframe(db.cypher_query(query=query, params=params))
    return df


def safe_execute_cypher_query(query: str, params: Optional[dict[str, Any]] = None) -> DataFrame:
    keywords = ["create", "set", "merge", "detach", "delete", "remove"]

    if any([keyword in query.lower() for keyword in keywords]):
        raise SafeExecutionException

    return execute_cypher_query(query, params=params)

import pandas as pd

from pandas.core.frame import DataFrame

from neomodel import StructuredNode


def nodelist_to_dataframe(nodes: list[StructuredNode]) -> DataFrame:
    df = pd.DataFrame.from_dict([node.serialize for node in nodes])
    return df

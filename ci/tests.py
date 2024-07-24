import pandas as pd
import pytest
import numpy as np

from .utils import cmor_tables, tables


@pytest.mark.parametrize("dreq_file", tables)
def test_all_in_cmor_tables(dreq_file):
    """test if all entries of a data request are registered in the cmor tables"""
    cmor_df = pd.read_csv(cmor_tables)
    dreq_df = pd.read_csv(dreq_file).drop(columns="priority")
    # dreq_df.loc[0, "out_name"] = "xxx"
    # merge two dataFrames and add indicator column
    all_df = pd.merge(
        dreq_df, cmor_df, on=dreq_df.columns.to_list(), how="left", indicator="exists"
    )
    all_df["exists"] = np.where(all_df.exists == "both", True, False)
    if not all_df.exists.all():
        print(
            "!!!! There are some variables from {dreq_file} that do not exsits in cmor tables !!!!"
        )
        print(print(all_df[~all_df.exists]))

    assert all_df.exists.all()

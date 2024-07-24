import pandas as pd
import pytest
import numpy as np

from .utils import cmor_tables, tables


@pytest.mark.parametrize("dreq_file", tables)
def test_no_duplicates(dreq_file):
    """assert all entries of a data request are unique"""
    dreq_df = pd.read_csv(dreq_file)
    assert dreq_df.loc[dreq_df.duplicated()].empty
    assert (
        dreq_df.drop(columns="priority")
        .loc[dreq_df.drop(columns="priority").duplicated()]
        .empty
    )


@pytest.mark.parametrize("dreq_file", tables)
def test_all_in_cmor_tables(dreq_file):
    """assert all entries of a data request are registered in the cmor tables"""
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
            f"!!!! There are some variables from {dreq_file} that do not exsits in cmor tables !!!!"
        )
        print(print(all_df[~all_df.exists]))

    assert all_df.exists.all()

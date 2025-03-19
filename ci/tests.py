import numpy as np
import pandas as pd
import pytest
from cf_xarray.utils import parse_cf_standard_name_table
from .utils import cmor_tables, tables


@pytest.mark.parametrize("dreq_file", tables)
def test_no_duplicates(dreq_file):
    """
    Ensure all entries in the data request file are unique.

    This test checks that there are no duplicate entries in the data request file.
    It verifies uniqueness both with and without the 'priority' column.
    """
    dreq_df = pd.read_csv(dreq_file)
    assert dreq_df.loc[dreq_df.duplicated()].empty
    assert (
        dreq_df.drop(columns="priority")
        .loc[dreq_df.drop(columns="priority").duplicated()]
        .empty
    )


@pytest.mark.parametrize("dreq_file", tables)
def test_all_in_cmor_tables(dreq_file):
    """
    Ensure all entries in the data request file are registered in the CMOR tables.

    This test checks that every entry in the data request file exists in the CMOR tables.
    It merges the data request file with the CMOR tables and verifies that all entries are present.
    """
    print(f"Checking if all entries exist in CMOR table: {dreq_file}")
    cmor_df = pd.read_csv(cmor_tables)
    dreq_df = pd.read_csv(dreq_file).drop(columns=["comment", "priority"])
    # dreq_df.loc[0, "out_name"] = "xxx"
    # Merge two DataFrames and add indicator column
    all_df = pd.merge(
        dreq_df, cmor_df, on=dreq_df.columns.to_list(), how="left", indicator="exists"
    )
    all_df["exists"] = np.where(all_df.exists == "both", True, False)
    if not all_df.exists.all():
        print(
            f"!!!! There are some variables from {dreq_file} that do not exist in CMOR tables !!!!"
        )
        print(all_df[~all_df.exists])

    assert all_df.exists.all()
    print(f"Seems ok: {dreq_file}")


def test_all_positive_attrs_set():
    """
    Ensure all positive attributes are set in the CMOR tables.

    This test checks if the 'positive' attribute is set for all directional variables
    in the CMOR tables, as indicated by their standard names.
    """
    up = ["outgoing", "upward", "upwelling"]
    down = ["incoming", "downward", "downwelling", "sinking"]
    df = pd.read_csv(cmor_tables)

    ups = df.loc[df.standard_name.str.contains("|".join(up), case=False)]
    downs = df.loc[df.standard_name.str.contains("|".join(down), case=False)]

    assert all(ups.positive == "up")
    assert all(downs.positive == "down")


def test_cell_methods_attrs_set():
    """
    Ensure all cell methods attributes are set in the CMOR tables.

    This test checks if the 'cell_methods' attribute is set for all entries
    in the CMOR tables. It identifies any entries that are missing this attribute.
    """
    df = pd.read_csv(cmor_tables)

    no_cell_methods = df.loc[df.cell_methods.isna()]
    if not no_cell_methods.empty:
        print(
            f"No cell methods defined for: {no_cell_methods[['out_name', 'frequency', 'realm']]}"
        )

    assert no_cell_methods.empty


def test_dimensions_attrs_set():
    """
    Ensure all dimensions attributes are set in the CMOR tables.

    This test checks if the 'dimensions' attribute is set for all entries
    in the CMOR tables. It identifies any entries that are missing this attribute
    and prints them out.
    """
    df = pd.read_csv(cmor_tables)

    no_dimensions = df.loc[df.dimensions.isna()]
    if not no_dimensions.empty:
        print(
            f"No dimensions defined for: {no_dimensions[['out_name', 'frequency', 'realm']]}"
        )

    assert no_dimensions.empty


def test_all_units_cf_conform():
    """
    Ensure all units are CF conform in the CMOR tables.

    This test checks if the 'units' attribute for all entries in the CMOR tables
    conforms to the CF conventions. It identifies any entries with non-conforming units.
    """
    import cf_units

    def is_cf_conform(unit):
        try:
            cf_units.Unit(unit)
            return True
        except ValueError:
            return False

    df = pd.read_csv(cmor_tables)
    df["cf_units_conform"] = df["units"].apply(is_cf_conform)
    non_cf_units = df.loc[~df.cf_units_conform]
    if not non_cf_units.empty:
        print(f"Non CF conform units: {non_cf_units[['out_name', 'units']]}")
    assert non_cf_units.empty


def test_all_standard_names_cf_conform():
    """
    This test verifies that the 'standard_name' attribute for all entries in the CMOR tables
    matches the CF standard name table. It parses the CF standard name table and compares
    it against the 'standard_name' column in the CMOR tables. Any entries with non-conforming
    or missing standard names are flagged as errors.
    """
    # source = "https://raw.githubusercontent.com/cf-convention/cf-convention.github.io/master/Data/cf-standard-names/current/src/cf-standard-name-table.xml"
    info, table, aliases = parse_cf_standard_name_table()
    valid = list(table.keys()) + list(aliases.keys())
    df = pd.read_csv(cmor_tables)
    non_cf_standard_names = df.loc[~df.standard_name.isin(valid)][
        ["out_name", "standard_name", "realm"]
    ].drop_duplicates()

    if not non_cf_standard_names.empty:
        print(
            f"Non CF conform standard names: {non_cf_standard_names.standard_name.to_list()}"
        )
    assert non_cf_standard_names.empty

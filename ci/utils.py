import pandas as pd
from os import path as op
import glob
import re
import yaml

cmor_tables = "cmor-table/datasets.csv"
table_dir = "data-request"

cols = ["out_name", "standard_name", "long_name", "units", "cell_methods"]

tables = glob.glob(op.join(table_dir, "*.csv"))


def parse_cell_methods(cm_string):
    # https://stackoverflow.com/questions/52340963/how-to-insert-a-newline-character-before-a-words-that-contains-a-colon
    ys = re.sub(r"(\w+):", r"\n\1:", cm_string).strip()
    d = yaml.safe_load(ys)

    if "area" in d and d.get("area") is None:
        d["area"] = d["time"]

    return d


def parse_area_type(area=None):
    if area is None:
        return None
    split = area.split(" ")
    if len(split) == 3 and split[1] == "where":
        return split[2]
    else:
        return None


def human_readable(df):
    return df.groupby(cols)["frequency"].apply(list).to_frame()  # .reset_index()


def create_excel(filename):
    """create human readable excel file with one sheet per periority"""

    df = pd.read_csv(filename)
    sheets = {k: human_readable(v) for k, v in df.groupby("priority")}

    stem, suffix = op.splitext(filename)
    xlsxfile = f"{stem}.xlsx"

    with pd.ExcelWriter(xlsxfile) as writer:
        for k, v in sheets.items():
            v.to_excel(writer, sheet_name=k, index=True)
            nlevels = v.index.nlevels + len(v.columns)
            worksheet = writer.sheets[k]  # pull worksheet object
            for i in range(nlevels):
                worksheet.set_column(i, i, 40)

    return xlsxfile


def main():
    for filename in tables:
        print(f"creating excel table for: {filename}")
        xlsx = create_excel(filename)
        print(f"created: {xlsx}")


if __name__ == "__main__":
    print(f"found tables: {tables}")
    main()

import pandas as pd
from os import path as op
import glob

cmor_tables = "cmor-table/datasets.csv"
table_dir = "data-request"

cols = ["out_name", "standard_name", "long_name", "units", "cell_methods"]

tables = glob.glob(op.join(table_dir, "*.csv"))


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

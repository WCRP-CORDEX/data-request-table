import pandas as pd
from os import path as op

cols = ["out_name", "standard_name", "long_name", "units", "cell_methods"]


def human_readable(df):
    return df.groupby(cols)["frequency"].apply(list).to_frame()  # .reset_index()


def create_excel(filename):
    """create human readable excel file with one sheet per periority"""

    df = pd.read_csv(filename)
    sheets = {k: human_readable(v) for k, v in df.groupby("priority")}

    stem, suffix = op.splitext(filename)
    xlsxfile = "{stem}.xlsx"

    with pd.ExcelWriter(xlsxfile) as writer:
        for k, v in sheets.items():
            v.to_excel(writer, sheet_name=k, index=True)
            nlevels = v.index.nlevels + len(v.columns)
            worksheet = writer.sheets[k]  # pull worksheet object
            for i in range(nlevels):
                worksheet.set_column(i, i, 40)

    return xlsxfile

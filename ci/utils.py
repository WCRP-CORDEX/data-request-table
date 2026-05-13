import pandas as pd
from os import path as op
import glob
import os
import re
import yaml
from html import escape

cmor_tables = "cmor-table/datasets.csv"
table_dir = "data-request"
html_dir = "docs"

cols = ["out_name", "standard_name", "long_name", "units", "cell_methods"]

tables = sorted(glob.glob(op.join(table_dir, "*.csv")))

DATATABLE_CSS = "https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css"
JQUERY_JS = "https://code.jquery.com/jquery-3.5.1.js"
DATATABLE_JS = "https://cdn.datatables.net/1.11.5/js/jquery.dataTables.js"


def parse_cell_methods(cm_string):
    # https://stackoverflow.com/questions/52340963/how-to-insert-a-newline-character-before-a-words-that-contains-a-colon
    ys = re.sub(r"(\w+):", r"\n\1:", cm_string).strip()
    d = yaml.safe_load(ys)

    if "area" in d and d.get("area") is None:
        d["area"] = d["time"]

    return d


def parse_area_type(area=None):
    if not isinstance(area, str):
        return None
    split = area.split(" ")
    if len(split) == 3 and split[1] == "where":
        return split[2]
    else:
        return None


def human_readable(df):
    return df.groupby(cols)["frequency"].apply(list).to_frame()  # .reset_index()


def table_label(filename):
    stem = op.splitext(op.basename(filename))[0]
    return stem.replace("dreq_", "")


def html_cell(value):
    if pd.isna(value):
        return ""

    text = escape(str(value))
    if str(value).startswith(("http://", "https://")):
        return f'<a href="{text}">{text}</a>'
    return text


def navigation_html(current_file):
    links = []
    for filename in tables:
        label = table_label(filename)
        stem = op.splitext(op.basename(filename))[0]
        links.append(f'<a class="nav-button" href="{stem}.html">{escape(label)}</a>')
    return "".join(links)


def create_html(filename):
    df = pd.read_csv(filename).fillna("")

    stem = op.splitext(op.basename(filename))[0]
    os.makedirs(html_dir, exist_ok=True)
    htmlfile = op.join(html_dir, f"{stem}.html")
    label = table_label(filename)
    title = f"CORDEX-CMIP6 data request (<span style='color: #0969da;'>{label}</span>)"
    intro = (
        f"<div style='text-align: center; margin: 1em 0;'>{navigation_html(filename)}</div>"
        f"This is the CORDEX-CMIP6 RCM data request for {label}." 
        f" The browsable list shows the available variables, frequencies and other properties."
        f" For more information about the data request, see <a href='https://github.com/WCRP-CORDEX/data-request-table#tutorial'>https://github.com/WCRP-CORDEX/data-request-table</a>."
        f" CSV and Excel versions of the data request can be found <a href='https://github.com/WCRP-CORDEX/data-request-table/data-request'>here</a>."
    )

    header_html = "\n".join(f"        <th>{escape(column)}</th>" for column in df.columns)
    rows = []
    for _, row in df.iterrows():
        cells = "\n".join(f"        <td>{html_cell(row[column])}</td>" for column in df.columns)
        rows.append(f"      <tr>\n{cells}\n      </tr>")
    body_html = "\n".join(rows)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="author" content="J. Fernandez" />
    <meta name="keywords" content="HTML, CSS, JavaScript" />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="{DATATABLE_CSS}">
    <script type="text/javascript" charset="utf8" src="{JQUERY_JS}"></script>
    <script type="text/javascript" charset="utf8" src="{DATATABLE_JS}"></script>
    <style>
body {{
  font-family: "Montserrat", sans-serif;
  padding-top: 15px;
  padding-left: 15px;
  padding-right: 15px;
  padding-bottom: 600px;
}}
tr:hover {{background-color:#f5f5f5;}}
th, td {{text-align: left; padding: 2px;}}
table {{border-collapse: collapse;}}
span.tag {{
  background-color: #c5def5;
  padding: 0 10px;
  font-size: 12px;
  font-weight: 500;
  line-height: 22px !important;
  border: 1px solid transparent;
  border-radius: 2em;
}}
span.selected {{color: #3399FF}}
span.planned {{color: #F54d4d; font-weight: bold}}
span.running {{color: #009900; font-weight: bold}}
span.completed {{color: #17202a; font-weight: bold}}
span.published {{color: #3399FF; font-weight: bold}}
span.warning {{color: #FF0000; font-weight: bold}}
a {{color: DodgerBlue}}
a:link {{text-decoration: none; }}
a:visited {{ text-decoration: none; }}
a:hover {{text-decoration: underline; }}
a:active {{ text-decoration: underline; }}
.logo {{
  text-align: center;
  margin-bottom: 20px;
}}
.nav-button {{
  display: inline-block;
  padding: 8px 16px;
  margin: 0 4px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 20px;
  color: #0969da;
  text-decoration: none;
  transition: all 0.3s ease;
}}
.nav-button:hover {{
  background-color: #0969da;
  color: white;
  text-decoration: none;
}}
    </style>
</head>
<body>
    <div class="logo">
        <img src="https://cordex.org/wp-content/uploads/2025/02/CORDEX_RGB_logo_baseline_positive-300x133.png" alt="CORDEX Logo" >
        <h1>{title}</h1>
    </div>
    {intro}<p>
    <table id="table_id" class="display">
        <thead>
            <tr>
{header_html}
            </tr>
        </thead>
        <tbody>
{body_html}
        </tbody>
    </table>

    <script>
        function getParam(name) {{
            var urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(name) || '';
        }}

        function setParam(name, value) {{
            var url = new URL(window.location);
            if (value && value !== '') {{
                url.searchParams.set(name, value);
            }} else {{
                url.searchParams.delete(name);
            }}
            window.history.replaceState({{}}, '', url);
        }}

        $(document).ready(function() {{
            var initialSearch = getParam('search');
            var initialLength = parseInt(getParam('length'), 10) || 20;
            var initialOrder = getParam('order');
            var initialOrderArray = [[0, 'asc']];

            if (initialOrder) {{
                try {{
                    initialOrderArray = JSON.parse(initialOrder);
                }} catch (error) {{
                    console.log('Could not parse order parameter');
                }}
            }}

            var table = $('#table_id').DataTable({{
                pageLength: initialLength,
                lengthMenu: [20, 50, 100, 200, 500],
                order: initialOrderArray,
                searching: true
            }});

            if (initialSearch) {{
                table.search(initialSearch).draw();
            }}

            table.on('search.dt', function() {{
                setParam('search', table.search());
            }});

            table.on('length.dt', function(event, settings, len) {{
                setParam('length', len === 20 ? '' : len);
            }});

            table.on('order.dt', function() {{
                setParam('order', JSON.stringify(table.order()));
            }});
        }});
    </script>
</body>
</html>
"""

    with open(htmlfile, "w", encoding="utf-8") as fp:
        fp.write(html)

    return htmlfile


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
        print(f"creating html table for: {filename}")
        html = create_html(filename)
        print(f"created: {html}")


if __name__ == "__main__":
    print(f"found tables: {tables}")
    main()

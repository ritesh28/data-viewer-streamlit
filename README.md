# Data Viewer

A Streamlit app for exploring tabular data. Upload CSV or Excel, inspect summary stats and charts, filter and sort without changing the underlying data, then download CSV/Excel.

Inspired by [VS Code Data Wrangler](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.datawrangler); Edit mode and auto-generated Pandas cleaning code are planned next.

## Features

| Area               | What it does                                                                     |
| ------------------ | -------------------------------------------------------------------------------- |
| **Upload**         | Load `.csv` or `.xlsx`, or use **Load sample** for the included demo dataset     |
| **Explore panel**  | Tabs for **Summary**, **Insights**, and **Filters** beside the data grid         |
| **Data Summary**   | Dataset or per-column stats (missing, distinct, mean/median/min/max, top values) |
| **Quick Insights** | Distribution histogram (numeric) or frequency chart (categorical) via Plotly     |
| **Filters & Sort** | Non-destructive view overlays — working data is unchanged                        |
| **Data Grid**      | Always-visible scrollable table with filtered row counts (`N of total`)          |
| **Download**       | Export the full working dataset as CSV or Excel (not just the filtered view)     |

## Requirements

- Python **3.11+**
- [Poetry](https://python-poetry.org/) for dependencies

## Setup

```bash
pyenv local 3.11.7
pyenv exec python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools poetry
poetry install
```

## Run

```bash
poetry run streamlit run main.py
```

Open the URL Streamlit prints (default `http://localhost:8501`).

### Streamlit Cloud

Set the main file path to `main.py`. The project uses `package-mode = false` in `pyproject.toml` so Poetry installs dependencies only.

## Supported formats

| Action   | Formats         |
| -------- | --------------- |
| Upload   | `.csv`, `.xlsx` |
| Download | `.csv`, `.xlsx` |

Sample file: `Sample_Data_for_Plotting_and_Filtering.csv`

## Project layout

```text
main.py              # Streamlit entrypoint
app/
  state.py           # session state
  io.py              # CSV/Excel load & export
  stats.py           # summary statistics
  view_query.py      # non-destructive filter/sort
  ui/                # sidebar, summary, insights, filters, grid
```

## Roadmap

1. ~~Skeleton — upload, grid, download~~
2. ~~View mode — summary, insights, filter/sort~~
3. Edit mode shell — mode toggle, operations list, cleaning steps, code preview
4. Core / text / numeric transform operations
5. Diff highlighting, step undo/edit, polished code export

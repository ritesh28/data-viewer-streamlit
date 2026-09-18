# Data Viewer (Streamlit)

Tabular data viewer and cleaning tool.

**Current:** upload CSV/Excel, explore with summary stats / quick insights / non-destructive filter & sort, download as-is.

## Setup

```bash
pyenv local 3.11.7
pyenv exec python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools
pip install poetry
poetry install
```

## Run

```bash
poetry run streamlit run main.py
```

## Supported formats

| Action   | Formats         |
| -------- | --------------- |
| Upload   | `.csv`, `.xlsx` |
| Download | `.csv`, `.xlsx` |

Use **Load sample** in the sidebar to open `Sample_Data_for_Plotting_and_Filtering.csv` without uploading.

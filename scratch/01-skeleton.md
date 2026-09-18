# Milestone 01 — Skeleton

**Parent spec:** [projectV2.md](./projectV2.md)  
**Goal:** Upload CSV/Excel, show a dataframe in the UI, download the same data as-is.

This milestone establishes the app shell, file I/O, session-state foundations, and the first end-to-end loop. Later milestones (View mode, Edit mode, ops) build on this without reworking upload/download.

---

## Scope

### In scope

- Streamlit page config and basic layout (sidebar + main)
- File upload for `.csv`, `.xlsx`, `.xls`
- Parse upload into a Pandas `DataFrame`
- Persist data in `st.session_state`
- Display data with `st.dataframe` (scrollable grid)
- Show basic metadata: filename, shape (`rows × cols`), column names/dtypes
- Empty state when no file is loaded
- Clear / reset loaded data
- Download current dataframe as CSV and Excel (as-is — no transforms yet)
- Optional: load the sample CSV for local demos without uploading
- Dependencies: `pandas`, Excel engine (`openpyxl`)

### Out of scope (defer)

- View / Edit mode toggle
- Summary stats, Quick Insights, charts
- Filters, sorts, cleaning operations
- Cleaning Steps, Code Preview, diffs
- Generated Pandas code
- Multi-sheet Excel editing beyond a simple sheet picker (sheet picker is optional nice-to-have here)

---

## Success criteria

| #   | Criterion                                                                              |
| --- | -------------------------------------------------------------------------------------- |
| 1   | `streamlit run main.py` starts without errors                                          |
| 2   | User can upload the sample CSV and see all rows/columns in a grid                      |
| 3   | User can upload a simple `.xlsx` and see the same                                      |
| 4   | Download CSV produces a file that re-opens with the same shape                         |
| 5   | Download Excel produces a readable `.xlsx` with the same shape                         |
| 6   | Invalid/unsupported files show a clear error; app does not crash                       |
| 7   | Reloading the page (same session) keeps data until browser session ends or user clears |
| 8   | “Clear data” returns the app to the empty state                                        |

---

## Dependencies

Add via Poetry:

```bash
poetry add pandas openpyxl
```

| Package     | Why                           |
| ----------- | ----------------------------- |
| `pandas`    | DataFrame load/display/export |
| `openpyxl`  | Read/write `.xlsx`            |
| `streamlit` | Already present (`>=1.50.0`)  |

Notes:

- `.xls` (legacy) may need `xlrd`; **prefer documenting `.xlsx` + `.csv` only** unless you explicitly add `xlrd`. Recommendation for skeleton: accept `.csv` and `.xlsx` only.
- Use in-memory buffers (`io.BytesIO` / `io.StringIO`) for downloads — do not write temp files to disk.

---

## Proposed layout

Keep the first milestone in a small, readable structure. Prefer modules early so View/Edit mode do not dump everything into `main.py`.

```text
data-viewer-streamlit/
├── main.py                 # entry: page config + compose UI
├── app/
│   ├── __init__.py
│   ├── state.py            # session_state keys + init helpers
│   ├── io.py               # load / serialize CSV & Excel
│   └── ui/
│       ├── __init__.py
│       ├── sidebar.py      # upload, sample load, clear, downloads
│       └── grid.py         # dataframe display + metadata
├── Sample_Data_for_Plotting_and_Filtering.csv
├── pyproject.toml
└── scratch/
    ├── projectV2.md
    └── 01-skeleton.md      # this plan
```

**Minimal alternative:** if you want the absolute smallest first PR, implement everything in `main.py`, then extract modules before milestone 02. Prefer the modular layout above if you expect to continue immediately.

---

## Session state (foundation)

Initialize once at app start. Keys below are intentionally forward-compatible with later milestones.

| Key               | Type                      | Skeleton use                          | Later                |
| ----------------- | ------------------------- | ------------------------------------- | -------------------- |
| `df_raw`          | `pd.DataFrame \| None`    | Original upload (immutable copy)      | Reset / “revert all” |
| `df`              | `pd.DataFrame \| None`    | Working copy shown in grid            | Transforms land here |
| `source_name`     | `str \| None`             | Uploaded or sample filename           | Labels, export names |
| `source_type`     | `"csv" \| "xlsx" \| None` | Detected format                       | Re-export defaults   |
| `mode`            | `"view" \| "edit"`        | Set default `"view"`; UI toggle later | Milestone 03         |
| `cleaning_steps`  | `list`                    | Empty `[]`                            | Milestone 03+        |
| `selected_column` | `str \| None`             | `None`                                | View mode stats      |

**Rules for skeleton:**

1. On successful load: set `df_raw = df.copy()`, `df = df.copy()`, set `source_name` / `source_type`, reset `cleaning_steps = []`.
2. Grid and downloads always read from `df` (not `df_raw`), so future transforms automatically flow through.
3. Clear resets all keys above to their empty defaults.

```python
# app/state.py — conceptual sketch
DEFAULTS = {
    "df_raw": None,
    "df": None,
    "source_name": None,
    "source_type": None,
    "mode": "view",
    "cleaning_steps": [],
    "selected_column": None,
}

def init_state() -> None:
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, list) else value

def clear_data() -> None:
    for key, value in DEFAULTS.items():
        st.session_state[key] = value.copy() if isinstance(value, list) else value
```

---

## I/O design

### Load

| Input                 | Function                                               | Behavior                                                |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------- |
| Upload `UploadedFile` | `load_uploaded_file(file) -> tuple[pd.DataFrame, str]` | Infer type from name/suffix; return `(df, source_type)` |
| Sample path           | `load_sample(path) -> pd.DataFrame`                    | `pd.read_csv` on repo sample                            |

**CSV:** `pd.read_csv(file)` — rely on Pandas defaults for skeleton; do not add delimiter/encoding UI yet. Catch `UnicodeDecodeError` / `ParserError` and show `st.error`.

**Excel:** `pd.read_excel(file, engine="openpyxl")`.  
Optional: if multiple sheets, `st.selectbox` for sheet name after upload (nice-to-have). Default = first sheet.

### Download

| Format | Implementation                                                                  |
| ------ | ------------------------------------------------------------------------------- |
| CSV    | `df.to_csv(index=False)` → bytes / string → `st.download_button`                |
| Excel  | `df.to_excel(BytesIO(), index=False, engine="openpyxl")` → `st.download_button` |

Suggested download filenames:

- `{stem}_export.csv`
- `{stem}_export.xlsx`

where `stem` is `Path(source_name).stem` or `"data"` if missing.

---

## UI wireframe

```text
┌─────────────────────────────────────────────────────────┐
│  Data Viewer                                      [app] │
├──────────────┬──────────────────────────────────────────┤
│  SIDEBAR     │  MAIN                                    │
│              │                                          │
│  Upload      │  Empty: “Upload a CSV or Excel file…”    │
│  [file]      │                                          │
│              │  — or —                                  │
│  [Load       │                                          │
│   sample]    │  Header: filename · 100 rows × 6 cols    │
│              │                                          │
│  ───         │  st.dataframe(df, use_container_width)   │
│              │                                          │
│  Download    │  (optional expander: dtypes table)       │
│  [CSV] [XLSX]│                                          │
│              │                                          │
│  [Clear]     │                                          │
└──────────────┴──────────────────────────────────────────┘
```

### Sidebar behavior

1. **File uploader** — `type=["csv", "xlsx"]`. On change, parse and store in session state.
2. **Load sample** — button that loads `Sample_Data_for_Plotting_and_Filtering.csv` from the project root (resolve path relative to repo root / `__file__`).
3. **Download buttons** — disabled or hidden when `df is None`.
4. **Clear** — confirm via button click (Streamlit has no native confirm; a second “Confirm clear” or immediate clear is fine for skeleton).

### Main behavior

- If `df is None`: show `st.info` empty state with short instructions.
- If `df` present: title/caption with metadata + `st.dataframe(df, use_container_width=True, hide_index=True)`.
- Use `st.dataframe` (not `st.table`) so large frames stay scrollable/performant.

---

## Implementation steps

Work in this order. Each step should leave the app runnable.

### Step 0 — Dependencies & entry

1. `poetry add pandas openpyxl`
2. Confirm `streamlit run main.py` still launches
3. Set page config early in `main.py`:

```python
st.set_page_config(
    page_title="Data Viewer",
    page_icon="📊",  # or omit if you prefer no emoji
    layout="wide",
)
```

### Step 1 — Session state module

1. Create `app/state.py` with `init_state()` and `clear_data()`
2. Call `init_state()` at the top of `main.py` after page config

### Step 2 — I/O module

1. Create `app/io.py` with:
   - `load_uploaded_file(uploaded_file) -> tuple[pd.DataFrame, str]`
   - `dataframe_to_csv_bytes(df) -> bytes`
   - `dataframe_to_excel_bytes(df) -> bytes`
2. Centralize try/except; raise or return errors that UI can display as `st.error`
3. Unit-smoke locally: load sample path in a one-off Python REPL / small script if helpful

### Step 3 — Sidebar UI

1. Create `app/ui/sidebar.py` → `render_sidebar() -> None`
2. Wire uploader → on success update `df`, `df_raw`, `source_name`, `source_type`
3. Wire sample button and clear button
4. Wire download buttons using byte helpers

**Upload gotcha:** Streamlit re-runs the script on every interaction. Prefer loading when the uploaded file identity changes (e.g. compare `uploaded_file.name` + `uploaded_file.size` to last loaded), or load whenever a file is present and accept re-parse cost for skeleton. Document the choice in a short comment.

### Step 4 — Grid UI

1. Create `app/ui/grid.py` → `render_grid() -> None`
2. Empty state vs dataframe + metadata caption
3. Optional `st.expander("Column types")` with a small dtype table (`pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str)})`)

### Step 5 — Compose in `main.py`

```python
# conceptual
st.set_page_config(...)
init_state()
render_sidebar()
st.title("Data Viewer")
render_grid()
```

### Step 6 — Manual verification

Use the checklist below with the sample CSV and a tiny Excel file (export the sample once via the app, or create a 2×3 sheet in Sheets/Excel).

---

## Error handling

| Case                       | Expected UX                                                                                                |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| No file yet                | Info empty state; downloads hidden/disabled                                                                |
| Unsupported extension      | Uploader should block; if somehow passed, `st.error`                                                       |
| Corrupt CSV / bad encoding | `st.error` with short message; do not clear previous good `df` unless you choose to (prefer keep previous) |
| Corrupt Excel              | Same as corrupt CSV                                                                                        |
| Empty file (0 columns)     | Warn and reject load                                                                                       |
| Download with no data      | Buttons not shown                                                                                          |

Do not print raw stack traces in the UI; log/print to console if needed during development.

---

## Manual test checklist

- [ ] Fresh start shows empty state
- [ ] Upload `Sample_Data_for_Plotting_and_Filtering.csv` → grid shows 100 rows × 6 cols (verify against file)
- [ ] “Load sample” works without using the uploader
- [ ] Download CSV → re-upload that CSV → same shape (index not added as a column)
- [ ] Download Excel → open in Excel/Numbers or re-upload → same shape
- [ ] Upload a small `.xlsx` created externally
- [ ] Clear returns to empty state; downloads disappear
- [ ] Upload an invalid `.csv` (e.g. rename a `.png` to `.csv`) → error, app still usable
- [ ] Wide layout: grid uses full width; sidebar usable on a normal laptop viewport

---

## Acceptance demo script

1. Run `poetry run streamlit run main.py`
2. Click **Load sample**
3. Confirm caption shows expected rows/cols and grid is scrollable
4. Download CSV and Excel
5. Click **Clear**, then upload the downloaded CSV
6. Confirm data returns

---

## Definition of done

- Modular (or intentionally single-file) skeleton merged/ready locally
- Dependencies locked in `poetry.lock`
- All success criteria and manual checklist items pass
- No View/Edit chrome yet — avoid building panels that will be redesigned in milestones 02–03
- Brief note in README: how to run + supported formats (optional but useful)

---

## Handoff to Milestone 02 (View mode)

After skeleton, `df` / `df_raw` exist and the grid is stable. Milestone 02 should add:

- Data Summary panel
- Quick Insights header
- Non-destructive filter/sort (view overlays — do not overwrite `df_raw`)

Do not invent cleaning steps or mode toggle until milestone 03 unless needed for layout scaffolding.

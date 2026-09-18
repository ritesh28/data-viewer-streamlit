# Data Viewer — Streamlit Project Spec (v2)

A tabular data viewer and cleaning tool built with **Python + Streamlit**. Users upload CSV/Excel, explore and transform data in a rich UI, and get **auto-generated Pandas code** for every cleaning step.

---

## Goals

- Upload CSV or Excel and inspect data in an interactive grid
- Explore columns with summary statistics and quick visual insights
- Filter and sort for initial exploration (View mode)
- Apply cleaning/transform operations with live preview (Edit mode)
- Maintain a reversible history of cleaning steps with generated Pandas code
- Download processed data as CSV or Excel, and copy/export generated code

---

## Tech stack

| Layer         | Choice                                                        |
| ------------- | ------------------------------------------------------------- |
| UI            | Streamlit                                                     |
| Data          | Pandas                                                        |
| File I/O      | CSV + Excel (openpyxl / xlsxwriter as needed)                 |
| Grid / charts | Streamlit dataframe widgets + Plotly (or Streamlit built-ins) |

Sample dataset for development: `Sample_Data_for_Plotting_and_Filtering.csv`

---

## Modes

The app has two modes. A clear toggle switches between them.

### View mode

Optimized for **exploration**: view, filter, and sort without mutating the dataset.

![View mode reference](./view%20mode.png)

| #   | Area                   | Behavior                                                                                                                              |
| --- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Data Summary**       | Dataset-level or selected-column statistics (count, missing, distinct, mean/median/min/max for numerics, top values for categoricals) |
| 2   | **Column header menu** | Filter and sort from each column header                                                                                               |
| 3   | **Mode toggle**        | Switch between View and Edit                                                                                                          |
| 4   | **Quick Insights**     | Per-column strip: distribution (numeric) or frequency (categorical), plus missing and distinct counts                                 |
| 5   | **Data Grid**          | Scrollable table of the full (or filtered) dataset                                                                                    |

### Edit mode

Optimized for **transforms**: apply operations, preview diffs, and accumulate reversible cleaning steps with code.

![Edit mode reference](./edit%20mode.png)

| #   | Area                  | Behavior                                                                                                                                            |
| --- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Operations panel**  | Searchable list of built-in operations, grouped by category                                                                                         |
| 2   | **Cleaning Steps**    | Ordered history of applied operations; undo any step; edit the latest (or selected) step; selecting a step highlights its effect and shows its code |
| 3   | **Export**            | Download cleaned data (CSV/Excel) and export generated Pandas code (clipboard / `.py` / notebook-friendly snippet)                                  |
| 4   | **Data diff overlay** | While previewing an operation, highlight changed/added/removed cells and rows in the grid                                                           |
| 5   | **Code Preview**      | Pandas code for the selected operation (empty if none selected); user can edit the code and see the grid update to match                            |

### Modifying previous steps

1. Select a step in **Cleaning Steps**
2. Change it via the Operations panel or by editing the Code Preview
3. Grid highlights the effect of the updated step relative to prior state

---

## Core flows

```text
Upload CSV/Excel
    → Parse into DataFrame (session state)
    → View mode: explore / filter / sort (non-destructive view filters)
    → Edit mode: apply operations → append to Cleaning Steps
    → Preview op → confirm → commit step + regenerate code
    → Export data and/or code
```

**Session state should hold:** raw DataFrame, current DataFrame, list of cleaning steps (params + generated code), selected column, active mode, pending preview operation.

---

## Operations catalog

Operations are applied in Edit mode and each successful apply becomes one Cleaning Step.

### Shape & columns

| Operation                     | Description                                   |
| ----------------------------- | --------------------------------------------- |
| Drop column                   | Delete one or more columns                    |
| Select column                 | Keep listed columns; drop the rest            |
| Rename column                 | Rename one or more columns                    |
| Clone column                  | Copy one or more columns                      |
| Change column type            | Cast column dtype                             |
| One-hot encode                | Expand categorical column into binary columns |
| Group by column and aggregate | Group-by + aggregations                       |

### Rows & missing data

| Operation           | Description                                      |
| ------------------- | ------------------------------------------------ |
| Sort                | Sort by one or more columns ascending/descending |
| Filter              | Keep rows matching one or more conditions        |
| Drop missing values | Remove rows with nulls (selected columns or any) |
| Fill missing values | Replace nulls with a constant or strategy        |
| Drop duplicate rows | Drop duplicates on selected columns              |

### Text

| Operation                  | Description                                     |
| -------------------------- | ----------------------------------------------- |
| Strip whitespace           | Trim leading/trailing whitespace                |
| Find and replace           | Replace matching pattern (literal or regex)     |
| Split text                 | Split column on delimiter into multiple columns |
| Calculate text length      | New column = string length                      |
| Capitalize first character | Title-style first char upper, rest lower        |
| Convert text to lowercase  | Lowercase                                       |
| Convert text to uppercase  | Uppercase                                       |

### Numeric

| Operation            | Description                    |
| -------------------- | ------------------------------ |
| Scale min/max values | Min–max scale a numeric column |
| Round                | Round to N decimal places      |
| Round down (floor)   | Floor to integer               |
| Round up (ceiling)   | Ceiling to integer             |

---

## UI / UX requirements

- Sidebar or top bar: file upload, mode toggle, export actions
- Main area: Data Summary + Quick Insights + Data Grid
- Edit mode adds: Operations panel, Cleaning Steps, Code Preview, diff highlighting
- View-mode filters/sorts should not permanently mutate data unless explicitly applied as Edit operations
- Empty states: no file uploaded, no steps yet, no operation selected
- Errors: clear messages for bad uploads, invalid casts, and failed user-edited code

---

## Export

| Export | Format                                                                    |
| ------ | ------------------------------------------------------------------------- |
| Data   | CSV, Excel (`.xlsx`)                                                      |
| Code   | Concatenated Pandas script for all Cleaning Steps; optional per-step view |

Generated code should be readable and runnable given `df` as the working DataFrame.

---

## Non-goals (v1)

- Multi-file joins / multi-sheet Excel editing beyond first sheet (or a simple sheet picker)
- Collaborative real-time editing
- Full SQL editor
- Training ML models inside the app

---

## Implementation milestones

1. **Skeleton** — upload CSV/Excel, show dataframe, download as-is
2. **View mode** — summary stats, quick insights, column filter/sort
3. **Edit mode shell** — mode toggle, operations list, empty cleaning steps + code panel
4. **Core ops** — drop/rename/select/clone, type change, missing/duplicates, filter/sort
5. **Text & numeric ops** — remaining catalog
6. **Diff + step editing** — preview highlight, undo, edit last/selected step
7. **Export polish** — full script export, Excel download, code copy

---

## Reference

UI layout and interaction model are inspired by [VS Code Data Wrangler](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.datawrangler); this project reimplements the experience as a standalone Streamlit app.

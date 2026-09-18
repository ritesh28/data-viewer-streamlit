"""View-mode Filters & Sort panel (Streamlit adaptation of column header menus)."""

from __future__ import annotations

from datetime import date, datetime

import pandas as pd
import streamlit as st

from app.state import next_filter_id
from app.stats import is_datetime_series, is_numeric_series
from app.view_query import ops_for_series

_NULL_OPS = {"is_null", "not_null"}


def _coerce_value(series: pd.Series, op: str, raw):
    if op in _NULL_OPS:
        return None
    if op == "in":
        return list(raw) if raw is not None else []
    if op == "between":
        return list(raw)

    if is_numeric_series(series):
        if raw is None or raw == "":
            raise ValueError("Enter a numeric value.")
        return float(raw)

    if is_datetime_series(series):
        if raw is None:
            raise ValueError("Enter a date value.")
        if isinstance(raw, datetime):
            return pd.Timestamp(raw)
        if isinstance(raw, date):
            return pd.Timestamp(raw)
        return pd.Timestamp(raw)

    return "" if raw is None else str(raw)


def _value_inputs(series: pd.Series, op: str, key_prefix: str):
    if op in _NULL_OPS:
        return None

    if op == "in":
        options = sorted(series.dropna().astype(str).unique().tolist())
        return st.multiselect("Values", options=options, key=f"{key_prefix}_in")

    if op == "between":
        if is_numeric_series(series):
            non_null = series.dropna()
            lo_default = float(non_null.min()) if len(non_null) else 0.0
            hi_default = float(non_null.max()) if len(non_null) else 1.0
            c1, c2 = st.columns(2)
            low = c1.number_input("Low", value=lo_default, key=f"{key_prefix}_lo")
            high = c2.number_input("High", value=hi_default, key=f"{key_prefix}_hi")
            return [low, high]
        if is_datetime_series(series):
            non_null = series.dropna()
            lo_default = non_null.min().date() if len(non_null) else date.today()
            hi_default = non_null.max().date() if len(non_null) else date.today()
            c1, c2 = st.columns(2)
            low = c1.date_input("From", value=lo_default, key=f"{key_prefix}_lo")
            high = c2.date_input("To", value=hi_default, key=f"{key_prefix}_hi")
            return [low, high]
        st.warning("Between is only supported for numeric and datetime columns.")
        return None

    if is_numeric_series(series):
        return st.number_input("Value", value=0.0, key=f"{key_prefix}_num")

    if is_datetime_series(series):
        non_null = series.dropna()
        default = non_null.min().date() if len(non_null) else date.today()
        return st.date_input("Value", value=default, key=f"{key_prefix}_date")

    return st.text_input("Value", value="", key=f"{key_prefix}_text")


def _format_rule(rule: dict) -> str:
    op = rule.get("op")
    column = rule.get("column")
    value = rule.get("value")
    if op in _NULL_OPS:
        return f"`{column}` {op.replace('_', ' ')}"
    return f"`{column}` {op} `{value}`"


def render_filters(df: pd.DataFrame) -> None:
    """Build non-destructive view filter/sort rules from the full working df."""
    # Explicit panel instead of Data Wrangler-style column header menus.
    with st.expander("Add filter", expanded=True):
        if df.empty or df.shape[1] == 0:
            st.caption("No columns available.")
        else:
            col_name = st.selectbox(
                "Column",
                options=[str(c) for c in df.columns],
                key="new_filter_column",
            )
            series = df[col_name]
            op_options = ops_for_series(series)
            op_labels = {label: key for key, label in op_options}
            op_label = st.selectbox(
                "Condition",
                options=[label for _, label in op_options],
                key="new_filter_op",
            )
            op = op_labels[op_label]
            raw_value = _value_inputs(series, op, "new_filter")

            if st.button("Add filter", key="add_filter_btn"):
                try:
                    value = _coerce_value(series, op, raw_value)
                    if op == "in" and not value:
                        st.warning("Select at least one value.")
                    else:
                        st.session_state.view_filters.append(
                            {
                                "id": next_filter_id(),
                                "column": col_name,
                                "op": op,
                                "value": value,
                            }
                        )
                        st.rerun()
                except ValueError as exc:
                    st.warning(str(exc))

    filters = st.session_state.view_filters
    if filters:
        st.markdown("**Active filters**")
        for rule in list(filters):
            c1, c2 = st.columns([6, 1])
            c1.markdown(_format_rule(rule))
            if c2.button("✕", key=f"rm_filter_{rule['id']}"):
                st.session_state.view_filters = [
                    f for f in filters if f.get("id") != rule["id"]
                ]
                st.rerun()
    else:
        st.caption("No filters applied.")

    st.markdown("**Sort**")
    sort_col = st.selectbox(
        "Sort by",
        options=["(none)", *[str(c) for c in df.columns]],
        key="sort_column_select",
    )
    sort_dir = st.radio(
        "Direction",
        options=["Ascending", "Descending"],
        horizontal=True,
        key="sort_direction",
    )

    if sort_col == "(none)":
        st.session_state.view_sort = []
    else:
        st.session_state.view_sort = [
            {"column": sort_col, "ascending": sort_dir == "Ascending"}
        ]

    if st.button("Clear filters & sort", type="secondary"):
        st.session_state.view_filters = []
        st.session_state.view_sort = []
        st.rerun()

"""Quick Insights charts for the selected column."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from app.stats import column_summary, is_datetime_series, is_numeric_series

MAX_CATEGORY_BARS = 30
TOP_N_CHART = 20


def render_insights(df_view: pd.DataFrame) -> None:
    """Charts and badges for selected_column, computed on df_view."""
    selected = st.session_state.selected_column

    if selected is None:
        st.caption("Select a column in Summary to see distribution insights.")
        return

    if selected not in df_view.columns:
        st.warning(f"Column '{selected}' is not in the current view.")
        return

    series = df_view[selected]
    summary = column_summary(series)
    st.caption(
        f"**{selected}** · Missing: {summary['missing']:,} · Distinct: {summary['distinct']:,}"
    )

    non_null = series.dropna()
    if non_null.empty:
        st.info("No non-null values to chart.")
        return

    if is_numeric_series(series):
        plot_df = pd.DataFrame({selected: non_null.astype(float)})
        chart = (
            alt.Chart(plot_df)
            .mark_bar()
            .encode(
                x=alt.X(f"{selected}:Q", bin=alt.Bin(maxbins=30), title=selected),
                y=alt.Y("count()", title="Count"),
            )
            .properties(height=240)
        )
        st.altair_chart(chart)
        return

    if is_datetime_series(series):
        dates = pd.to_datetime(non_null).dt.date.value_counts().sort_index()
        plot_df = dates.rename("count").rename_axis("date").reset_index()
        st.bar_chart(plot_df, x="date", y="count", height=240)
        return

    counts = non_null.astype(str).value_counts()
    if len(counts) > MAX_CATEGORY_BARS:
        st.caption(
            f"High cardinality ({len(counts):,} distinct). Showing top {TOP_N_CHART}."
        )
        counts = counts.head(TOP_N_CHART)
    elif len(counts) > TOP_N_CHART:
        counts = counts.head(TOP_N_CHART)
        st.caption(f"Showing top {TOP_N_CHART} values.")

    freq_df = counts.rename("count").rename_axis(selected).reset_index()
    st.bar_chart(
        freq_df,
        x="count",
        y=selected,
        horizontal=True,
        height=max(200, min(420, 28 * len(freq_df))),
    )

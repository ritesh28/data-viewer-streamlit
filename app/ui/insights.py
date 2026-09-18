"""Quick Insights charts for the selected column."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from app.stats import column_summary, is_datetime_series, is_numeric_series

MAX_CATEGORY_BARS = 30
TOP_N_CHART = 20


def render_insights(df_view: pd.DataFrame) -> None:
    """Charts and badges for selected_column, computed on df_view."""
    st.subheader("Quick Insights")
    selected = st.session_state.selected_column

    if selected is None:
        st.caption("Select a column in Data Summary to see distribution insights.")
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

    plot_df = pd.DataFrame({selected: non_null})

    if is_numeric_series(series) or is_datetime_series(series):
        fig = px.histogram(plot_df, x=selected, nbins=30 if is_numeric_series(series) else None)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280)
        st.plotly_chart(fig, use_container_width=True)
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

    freq_df = counts.reset_index()
    freq_df.columns = [selected, "count"]
    fig = px.bar(freq_df, x="count", y=selected, orientation="h")
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=max(220, 28 * len(freq_df)),
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(fig, use_container_width=True)

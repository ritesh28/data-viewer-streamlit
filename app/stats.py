"""Pure helpers for dataset and column summary statistics."""

from __future__ import annotations

from typing import Any

import pandas as pd


def is_numeric_series(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series)


def is_datetime_series(series: pd.Series) -> bool:
    return pd.api.types.is_datetime64_any_dtype(series)


def dataset_summary(df: pd.DataFrame) -> dict[str, Any]:
    rows, cols = df.shape
    missing_cells = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())
    dtype_counts = {
        "numeric": int(sum(is_numeric_series(df[c]) for c in df.columns)),
        "datetime": int(sum(is_datetime_series(df[c]) for c in df.columns)),
        "other": 0,
    }
    dtype_counts["other"] = cols - dtype_counts["numeric"] - dtype_counts["datetime"]
    return {
        "rows": rows,
        "columns": cols,
        "missing_cells": missing_cells,
        "duplicate_rows": duplicate_rows,
        "dtype_counts": dtype_counts,
    }


def column_summary(series: pd.Series) -> dict[str, Any]:
    total = len(series)
    missing = int(series.isna().sum())
    non_null = series.dropna()
    distinct = int(non_null.nunique())
    result: dict[str, Any] = {
        "count": total,
        "non_null": int(len(non_null)),
        "missing": missing,
        "missing_pct": (missing / total * 100.0) if total else 0.0,
        "distinct": distinct,
        "kind": "other",
    }

    if is_numeric_series(series):
        result["kind"] = "numeric"
        if len(non_null):
            result.update(
                {
                    "mean": float(non_null.mean()),
                    "median": float(non_null.median()),
                    "std": float(non_null.std()) if len(non_null) > 1 else 0.0,
                    "min": float(non_null.min()),
                    "max": float(non_null.max()),
                    "q25": float(non_null.quantile(0.25)),
                    "q75": float(non_null.quantile(0.75)),
                }
            )
        return result

    if is_datetime_series(series):
        result["kind"] = "datetime"
        if len(non_null):
            result["min"] = non_null.min()
            result["max"] = non_null.max()
        return result

    result["kind"] = "categorical"
    if len(non_null):
        top = non_null.astype(str).value_counts().head(5)
        result["top_values"] = [
            {"value": str(idx), "count": int(count)} for idx, count in top.items()
        ]
        lengths = non_null.astype(str).str.len()
        result["avg_str_length"] = float(lengths.mean())
    else:
        result["top_values"] = []
        result["avg_str_length"] = None
    return result

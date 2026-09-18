"""Non-destructive view filters and sorts over a DataFrame."""

from __future__ import annotations

from typing import Any

import pandas as pd

from app.stats import is_datetime_series, is_numeric_series


class ViewQueryWarning(Exception):
    """Collectable warning while applying a view rule."""


def _series_mask(series: pd.Series, op: str, value: Any) -> pd.Series:
    if op == "is_null":
        return series.isna()
    if op == "not_null":
        return series.notna()

    if op == "in":
        values = value if isinstance(value, (list, tuple, set)) else [value]
        return series.isin(list(values))

    if op in {"contains", "not_contains"}:
        as_str = series.astype(str)
        needle = "" if value is None else str(value)
        mask = as_str.str.contains(needle, case=False, na=False, regex=False)
        return ~mask if op == "not_contains" else mask

    if op == "between":
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ViewQueryWarning("Between filter requires a [low, high] value.")
        low, high = value
        return series.between(low, high, inclusive="both")

    if op == "eq":
        return series == value
    if op == "ne":
        return series != value
    if op == "gt":
        return series > value
    if op == "gte":
        return series >= value
    if op == "lt":
        return series < value
    if op == "lte":
        return series <= value

    raise ViewQueryWarning(f"Unknown filter operator: {op}")


def apply_view_query(
    df: pd.DataFrame,
    filters: list[dict] | None,
    sort_keys: list[dict] | None,
) -> tuple[pd.DataFrame, list[str]]:
    """Return (df_view, warnings). Never mutates the input frame."""
    result = df.copy()
    warnings: list[str] = []
    filters = filters or []
    sort_keys = sort_keys or []

    for rule in filters:
        column = rule.get("column")
        op = rule.get("op")
        if column not in result.columns:
            warnings.append(f"Skipped filter on missing column '{column}'.")
            continue
        try:
            mask = _series_mask(result[column], op, rule.get("value"))
            result = result.loc[mask]
        except ViewQueryWarning as exc:
            warnings.append(str(exc))
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Skipped filter on '{column}': {exc}")

    if sort_keys:
        by: list[str] = []
        ascending: list[bool] = []
        for key in sort_keys:
            column = key.get("column")
            if column not in result.columns:
                warnings.append(f"Skipped sort on missing column '{column}'.")
                continue
            by.append(column)
            ascending.append(bool(key.get("ascending", True)))
        if by:
            result = result.sort_values(by=by, ascending=ascending, kind="mergesort")

    return result, warnings


def ops_for_series(series: pd.Series) -> list[tuple[str, str]]:
    """Return (op_key, label) pairs appropriate for a column dtype."""
    base = [
        ("eq", "equals"),
        ("ne", "not equals"),
        ("is_null", "is missing"),
        ("not_null", "is not missing"),
        ("in", "is one of"),
    ]
    if is_numeric_series(series) or is_datetime_series(series):
        return base + [
            ("gt", "greater than"),
            ("gte", "greater or equal"),
            ("lt", "less than"),
            ("lte", "less or equal"),
            ("between", "between"),
        ]
    return base + [
        ("contains", "contains"),
        ("not_contains", "does not contain"),
    ]

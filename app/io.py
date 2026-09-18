"""Load and serialize tabular data (CSV / Excel)."""

from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO, Union

import pandas as pd

PathLike = Union[str, Path]
FileLike = Union[BinaryIO, PathLike]


class DataLoadError(Exception):
    """Raised when a file cannot be parsed into a usable DataFrame."""


def _validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.shape[1] == 0:
        raise DataLoadError("File has no columns.")
    return df


def _source_type_from_name(name: str) -> str:
    suffix = Path(name).suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".xlsx":
        return "xlsx"
    raise DataLoadError(f"Unsupported file type '{suffix}'. Use .csv or .xlsx.")


def load_csv(source: FileLike) -> pd.DataFrame:
    try:
        df = pd.read_csv(source)
    except UnicodeDecodeError as exc:
        raise DataLoadError("Could not decode CSV. Try saving the file as UTF-8.") from exc
    except pd.errors.ParserError as exc:
        raise DataLoadError(f"Could not parse CSV: {exc}") from exc
    except Exception as exc:  # noqa: BLE001 — surface a clean UI message
        raise DataLoadError(f"Could not read CSV: {exc}") from exc
    return _validate_dataframe(df)


def load_excel(source: FileLike, *, sheet_name: str | int = 0) -> pd.DataFrame:
    try:
        df = pd.read_excel(source, sheet_name=sheet_name, engine="openpyxl")
    except Exception as exc:  # noqa: BLE001
        raise DataLoadError(f"Could not read Excel file: {exc}") from exc
    return _validate_dataframe(df)


def load_uploaded_file(uploaded_file) -> tuple[pd.DataFrame, str]:
    """Parse a Streamlit UploadedFile. Returns (dataframe, source_type)."""
    source_type = _source_type_from_name(uploaded_file.name)
    # Rewind in case the buffer was read previously in this session.
    uploaded_file.seek(0)
    if source_type == "csv":
        df = load_csv(uploaded_file)
    else:
        df = load_excel(uploaded_file)
    return df, source_type


def load_sample(path: PathLike) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise DataLoadError(f"Sample file not found: {path}")
    return load_csv(path)


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()


def export_filename(source_name: str | None, extension: str) -> str:
    stem = Path(source_name).stem if source_name else "data"
    return f"{stem}_export.{extension.lstrip('.')}"

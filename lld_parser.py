"""Parse LLD spreadsheets (xlsx/csv) into structured data."""

import pandas as pd
from config import LLD_COLUMNS


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Map spreadsheet columns to normalized internal names."""
    col_map = {}
    for norm_key, variants in LLD_COLUMNS.items():
        for variant in variants:
            for col in df.columns:
                if col.strip().lower() == variant.strip().lower():
                    col_map[col] = norm_key
                    break
            if norm_key in col_map.values():
                break
    df = df.rename(columns=col_map)
    return df


def parse_lld(file) -> pd.DataFrame:
    """Read an uploaded file (xlsx or csv) and return a normalized DataFrame."""
    import io
    name = file.name.lower()
    # Read all bytes into memory immediately to avoid broken pipe
    # on Streamlit reruns (UploadedFile uses a socket-based buffer)
    file.seek(0)
    data = io.BytesIO(file.read())
    if name.endswith(".csv"):
        df = pd.read_csv(data)
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(data, engine="openpyxl")
    else:
        raise ValueError(f"Unsupported file type: {name}. Upload .xlsx or .csv")

    df = _normalize_columns(df)

    # Forward-fill module names (they're often merged cells)
    if "module_name" in df.columns:
        df["module_name"] = df["module_name"].ffill()

    # Drop completely empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    return df


def get_modules(df: pd.DataFrame) -> list:
    """Return unique module names."""
    if "module_name" not in df.columns:
        return ["All"]
    return df["module_name"].dropna().unique().tolist()


def get_lus_for_module(df: pd.DataFrame, module: str) -> pd.DataFrame:
    """Filter LUs belonging to a specific module."""
    if "module_name" not in df.columns:
        return df
    return df[df["module_name"] == module].reset_index(drop=True)


def lu_to_text(row: pd.Series) -> str:
    """Convert a single LU row into a rich text chunk for embedding/context."""
    parts = []

    fields = [
        ("module_name", "Module"),
        ("lu_sequence", "LU #"),
        ("lu_name", "LU Name"),
        ("learning_path", "Learning Path"),
        ("learning_objectives", "Learning Objectives"),
        ("learning_outcomes", "Learning Outcomes"),
        ("bridge_prev", "Bridge from Previous LU"),
        ("bridge_next", "Bridge to Next LU"),
        ("session_flow", "Session Flow (45 mins)"),
        ("fa_type", "Assessment Type"),
        ("assessment_details", "Assessment Details"),
        ("references", "References & Resources"),
        ("hld_mapping", "HLD Mapping"),
        ("level_of_effort", "Level of Effort"),
        ("note_for_authors", "Note for Authors"),
        ("completion_status", "Completion Status"),
    ]

    for key, label in fields:
        val = row.get(key, "")
        if pd.notna(val) and str(val).strip():
            parts.append(f"**{label}:** {str(val).strip()}")

    return "\n".join(parts)


def dataframe_to_chunks(df: pd.DataFrame) -> list[dict]:
    """Convert entire LLD dataframe into text chunks (one per LU) with metadata."""
    chunks = []
    for _, row in df.iterrows():
        text = lu_to_text(row)
        if len(text.strip()) < 20:
            continue
        meta = {
            "module": str(row.get("module_name", "Unknown")),
            "lu_seq": str(row.get("lu_sequence", "")),
            "lu_name": str(row.get("lu_name", "")),
        }
        chunks.append({"text": text, "metadata": meta})
    return chunks

import pandas as pd
from typing import Dict, Any


# --------------------------------
# Dataset basic information
# --------------------------------
def dataset_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Returns basic information about the dataset.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary with rows, columns, and column names.
    """
    rows, cols = df.shape

    return {
        "rows": rows,
        "columns": cols,
        "column_names": list(df.columns)
    }


# --------------------------------
# Missing values report
# --------------------------------
def missing_values_report(df: pd.DataFrame) -> Dict[str, int]:
    """
    Reports the number of missing values per column.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary with column names as keys and missing counts as values.
    """
    missing = df.isnull().sum()

    report = missing[missing > 0]

    return report.to_dict()


# --------------------------------
# Duplicate rows report
# --------------------------------
def duplicate_rows(df: pd.DataFrame) -> int:
    """
    Counts the number of duplicate rows.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        The number of duplicate rows.
    """
    duplicates = df.duplicated().sum()

    return duplicates


# --------------------------------
# Column data types
# --------------------------------
def column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Returns the data types of each column.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary with column names as keys and types as values.
    """
    return df.dtypes.astype(str).to_dict()


# --------------------------------
# Numeric summary statistics
# --------------------------------
def numeric_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Provides summary statistics for numeric columns.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary with summary statistics.
    """
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return {}

    summary = numeric_df.describe()

    return summary.to_dict()


# --------------------------------
# Full data quality report
# --------------------------------
def data_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generates a comprehensive data quality report.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary containing all quality metrics.
    """
    report = {
        "dataset_info": dataset_info(df),
        "missing_values": missing_values_report(df),
        "duplicate_rows": duplicate_rows(df),
        "column_types": column_types(df),
        "numeric_summary": numeric_summary(df)
    }

    return report

# Full data quality report


def advanced_quality_score(df):
    total_rows = len(df)
    total_cells = df.shape[0] * df.shape[1]

    # 1. Missing values
    missing = df.isnull().sum().sum()
    missing_pct = (missing / total_cells) * 100 if total_cells else 0

    # 2. Duplicate rows
    duplicates = df.duplicated().sum()
    duplicate_pct = (duplicates / total_rows) * 100 if total_rows else 0

    # 3. Empty strings
    empty_cells = (df == "").sum().sum()
    empty_pct = (empty_cells / total_cells) * 100 if total_cells else 0

    # 4. Inconsistent text (simple: uppercase)
    inconsistent = 0
    for col in df.select_dtypes(include='object'):
        inconsistent += df[col].str.contains(r"[A-Z]", na=False).sum()
    inconsistent_pct = (inconsistent / total_cells) * 100 if total_cells else 0

    # 5. Special characters
    special = 0
    for col in df.select_dtypes(include='object'):
        special += df[col].str.contains(r"[^a-zA-Z0-9 ]", na=False).sum()
    special_pct = (special / total_cells) * 100 if total_cells else 0

    # 6. Negative values
    negative = 0
    for col in df.select_dtypes(include='number'):
        negative += (df[col] < 0).sum()
    negative_pct = (negative / total_cells) * 100 if total_cells else 0

    # 7. Outliers (IQR)
    outliers = 0
    for col in df.select_dtypes(include='number'):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers += ((df[col] < (Q1 - 1.5*IQR)) |
                     (df[col] > (Q3 + 1.5*IQR))).sum()
    outlier_pct = (outliers / total_cells) * 100 if total_cells else 0

    # 8. Invalid dates
    invalid_dates = 0
    for col in df.columns:
        try:
            converted = pd.to_datetime(df[col], errors='coerce')
            invalid_dates += converted.isna().sum()
        except:
            pass
    invalid_date_pct = (invalid_dates / total_cells) * \
        100 if total_cells else 0

    # TOTAL SCORE
    total_issues = (missing_pct + duplicate_pct + empty_pct +
                    inconsistent_pct + special_pct +
                    negative_pct + outlier_pct + invalid_date_pct)

    score = max(0, 100 - total_issues)
    return {
        "score": round(score, 2),
        "missing": round(missing_pct, 2),
        "duplicates": round(duplicate_pct, 2),
        "empty": round(empty_pct, 2),
        "inconsistent": round(inconsistent_pct, 2),
        "special": round(special_pct, 2),
        "negative": round(negative_pct, 2),
        "outliers": round(outlier_pct, 2),
        "invalid_dates": round(invalid_date_pct, 2)
    }


def find_high_correlation(df, threshold=0.9):
    import numpy as np

    corr = df.corr(numeric_only=True)
    results = []

    for i in range(len(corr.columns)):
        for j in range(i):
            if abs(corr.iloc[i, j]) > threshold:
                col1 = corr.columns[i]
                col2 = corr.columns[j]
                value = round(corr.iloc[i, j], 2)

                results.append(f"{col1} ↔ {col2} ({value})")

    return results

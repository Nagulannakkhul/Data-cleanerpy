import pandas as pd
import numpy as np
import re


class DataCleaner:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    # -----------------------------
    # Remove duplicate rows
    # -----------------------------
    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self.df

    # -----------------------------
    # Remove empty rows
    # -----------------------------
    def remove_empty_rows(self):
        self.df = self.df.dropna(how="all")
        return self.df

    # -----------------------------
    # Remove rows with empty cells
    # -----------------------------
    def remove_empty_cells(self):
        self.df = self.df.dropna()
        return self.df

    # -----------------------------
    # Strip whitespace
    # -----------------------------
    def strip_spaces(self):
        self.df = self.df.map(
            lambda x: x.strip() if isinstance(x, str) else x
        )
        return self.df

    # -----------------------------
    # Remove special characters
    # -----------------------------
    def remove_special_characters(self):
        self.df = self.df.map(
            lambda x: re.sub(r"[^a-zA-Z0-9 ]", "",
                             x) if isinstance(x, str) else x
        )
        return self.df

    # -----------------------------
    # Outlier cleaning (IQR)
    # -----------------------------
    def remove_outliers_iqr(self):

        numeric_cols = self.df.select_dtypes(include=np.number)

        for col in numeric_cols:

            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            self.df = self.df[(self.df[col] >= lower) &
                              (self.df[col] <= upper)]

        return self.df

    # -----------------------------
    # Overbound cleaning
    # -----------------------------
    def overbound_clean(self, min_val=None, max_val=None):

        numeric_cols = self.df.select_dtypes(include=np.number)

        for col in numeric_cols:

            if min_val is not None:
                self.df = self.df[self.df[col] >= min_val]

            if max_val is not None:
                self.df = self.df[self.df[col] <= max_val]

        return self.df

    # -----------------------------
    # Fill missing values
    # -----------------------------
    def fill_missing_values(self):
        for col in self.df.columns:
            if self.df[col].dtype in ['int64', 'float64']:
                self.df[col].fillna(self.df[col].median(), inplace=True)
            else:
                self.df[col].fillna(self.df[col].mode()[
                                    0] if not self.df[col].mode().empty else '', inplace=True)
        return self.df

    # -----------------------------
    # Auto convert data types
    # -----------------------------
    def auto_convert_types(self):
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    # Try to convert to numeric
                    pd.to_numeric(self.df[col])
                    self.df[col] = pd.to_numeric(self.df[col])
                except ValueError:
                    try:
                        # Try to convert to datetime
                        pd.to_datetime(self.df[col])
                        self.df[col] = pd.to_datetime(self.df[col])
                    except ValueError:
                        pass  # Keep as string
        return self.df
    # -----------------------------
    # Fix Inconsistent Text
    # -----------------------------

    def fix_inconsistent_text(self):
        for col in self.df.select_dtypes(include='object'):
            self.df[col] = self.df[col].str.lower().str.strip()
        return self.df

    # -----------------------------
    # Remove Negative Values
    # -----------------------------
    def remove_negative_values(self):
        numeric_cols = self.df.select_dtypes(include=['number']).columns

        for col in numeric_cols:
            self.df = self.df[self.df[col] >= 0]
        return self.df

    # -----------------------------
    # Fix Invalid Dates
    # -----------------------------
    def fix_invalid_dates(self):
        for col in self.df.columns:
            try:
                converted = pd.to_datetime(self.df[col], errors='coerce')

                # If many values converted → treat as date column
                if converted.notna().sum() > len(self.df) * 0.5:
                    self.df[col] = converted
                    self.df = self.df[self.df[col].notna()]
            except:
                pass

    # -----------------------------
    # remove_high_correlation
    # -----------------------------
    def remove_high_correlation(self, threshold=0.9):
        import numpy as np

        corr = self.df.corr(numeric_only=True)

        upper = corr.where(~np.tril(np.ones(corr.shape)).astype(bool))

        to_drop = [col for col in upper.columns if any(upper[col] > threshold)]

        self.df.drop(columns=to_drop, inplace=True)

    # -----------------------------
    # Get cleaned dataframe
    # -----------------------------

    def get_data(self):
        return self.df

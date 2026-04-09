import customtkinter as ctk
from components.step_indicator import StepIndicator
import pandas as pd
import numpy as np
from llm_cleaner import analyze_data, smart_clean
import re
from data_cleaner import DataCleaner


class CleanPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Configure grid for flexibility
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # step
        self.grid_rowconfigure(1, weight=0)  # title
        self.grid_rowconfigure(2, weight=0)  # options frame
        self.grid_rowconfigure(3, weight=0)  # bound frame
        self.grid_rowconfigure(4, weight=0)  # buttons
        self.grid_rowconfigure(5, weight=0)  # status

        # STEP INDICATOR
        step = StepIndicator(self, current_step=2)
        step.grid(row=0, column=0, sticky="ew", pady=(20, 20))

        # TITLE
        title = ctk.CTkLabel(
            self, text="Select Cleaning Options", font=("Arial", 24, "bold"))
        title.grid(row=1, column=0, sticky="ew", pady=(15, 25))

        # -------------------------
        # Cleaning Options Frame
        # -------------------------
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row=2, column=0, sticky="ew",
                           pady=(15, 25), padx=15)

        self.remove_duplicates = ctk.BooleanVar()
        self.remove_empty_rows = ctk.BooleanVar()
        self.remove_empty_cells = ctk.BooleanVar()
        self.strip_spaces = ctk.BooleanVar()
        self.remove_special_chars = ctk.BooleanVar()
        self.outlier_clean = ctk.BooleanVar()
        self.fill_missing = ctk.BooleanVar()
        self.convert_types = ctk.BooleanVar()
        self.fix_case = ctk.BooleanVar()
        self.remove_negative = ctk.BooleanVar()
        self.fix_dates = ctk.BooleanVar()
        self.remove_corr = ctk.BooleanVar()

        options = [
            ("Remove Duplicate Rows", self.remove_duplicates),
            ("Remove Empty Rows", self.remove_empty_rows),
            ("Remove Rows With Empty Cells", self.remove_empty_cells),
            ("Strip Whitespace", self.strip_spaces),
            ("Remove Special Characters", self.remove_special_chars),
            ("Outlier Cleaning (IQR)", self.outlier_clean),
            ("Fill Missing Values (Mean/Median)", self.fill_missing),
            ("Auto Convert Data Types", self.convert_types),
            ("Fix Inconsistent Text (Case)", self.fix_case),
            ("Remove Negative Values", self.remove_negative),
            ("Fix Invalid Dates", self.fix_dates),
            ("Remove Highly Correlated Columns", self.remove_corr),
        ]

        # Create 2 column layout
        for i, (text, var) in enumerate(options):

            checkbox = ctk.CTkCheckBox(
                options_frame,
                text=text,
                variable=var,
                width=220
            )

            row = i // 2
            col = i % 2

            checkbox.grid(row=row, column=col, padx=30, pady=12, sticky="w")

        # -------------------------
        # Overbound Section
        # -------------------------
        bound_frame = ctk.CTkFrame(self)
        bound_frame.grid(row=3, column=0, sticky="ew", pady=(15, 25), padx=15)

        bound_label = ctk.CTkLabel(
            bound_frame, text="Overbound Cleaning", font=("Arial", 18, "bold"))
        bound_label.grid(row=0, column=0, columnspan=2, pady=(15, 15))

        self.min_entry = ctk.CTkEntry(
            bound_frame, placeholder_text="Min Value", width=130, height=30)
        self.min_entry.grid(row=1, column=0, padx=(15, 8), pady=(0, 15))

        self.max_entry = ctk.CTkEntry(
            bound_frame, placeholder_text="Max Value", width=130, height=30)
        self.max_entry.grid(row=1, column=1, padx=(8, 15), pady=(0, 15))

        # -------------------------
        # Buttons
        # -------------------------
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        button_frame.grid(row=4, column=0, sticky="ew", pady=(25, 30))

        back_btn = ctk.CTkButton(
            button_frame,
            text="Back",
            width=100,
            height=35,
            font=("Arial", 12),
            hover_color="red",
            command=lambda: controller.show_frame("UploadPage")
        )
        back_btn.grid(row=1, column=1, padx=15)

        clean_btn = ctk.CTkButton(
            button_frame,
            text="Apply Cleaning",
            width=100,
            height=35,
            font=("Arial", 12),
            hover_color="#4444FF",  # Blue for action
            command=self.clean_data
        )
        clean_btn.grid(row=0, column=1, padx=15)

        undo_btn = ctk.CTkButton(
            button_frame,
            text="Undo Changes",
            width=100,
            height=35,
            font=("Arial", 12),
            hover_color="#FFAA44",  # Orange for undo
            command=self.undo_changes
        )
        undo_btn.grid(row=0, column=2, padx=15)

        next_btn = ctk.CTkButton(
            button_frame,
            text="Next",
            width=100,
            height=35,
            font=("Arial", 12),
            hover_color="#44FF44",  # Green for next
            command=lambda: controller.show_frame("SavePage")
        )
        next_btn.grid(row=1, column=4, padx=15)

    # Ai Button
        ai_btn = ctk.CTkButton(
            button_frame,
            text="🤖 AI Clean",
            width=100,
            height=35,
            font=("Arial", 12),
            hover_color="#AA44FF",
            command=self.run_ai_clean
        )
        ai_btn.grid(row=0, column=4, padx=15)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.grid(row=5, column=0, sticky="ew", pady=(10, 20))

    # -------------------------
    # Cleaning Logic
    # -------------------------

    def clean_data(self):

        df = self.controller.df

        if df is None:
            self.status_label.configure(text="No dataset loaded")
            return

        try:
            cleaner = DataCleaner(df.copy())  # Work on a copy

            if self.remove_duplicates.get():
                cleaner.remove_duplicates()

            if self.remove_empty_rows.get():
                cleaner.remove_empty_rows()

            if self.remove_empty_cells.get():
                cleaner.remove_empty_cells()

            if self.strip_spaces.get():
                cleaner.strip_spaces()

            if self.remove_special_chars.get():
                cleaner.remove_special_characters()

            if self.outlier_clean.get():
                cleaner.remove_outliers_iqr()

            if self.fill_missing.get():
                cleaner.fill_missing_values()

            if self.convert_types.get():
                cleaner.auto_convert_types()

            if self.fix_case.get():
                cleaner.fix_inconsistent_text()

            if self.remove_negative.get():
                cleaner.remove_negative_values()

            if self.fix_dates.get():
                cleaner.fix_invalid_dates()
            if self.remove_corr.get():
                cleaner.remove_high_correlation()

            # Overbound cleaning
            min_val = self.min_entry.get()
            max_val = self.max_entry.get()

            if min_val or max_val:
                min_v = float(min_val) if min_val else None
                max_v = float(max_val) if max_val else None
                cleaner.overbound_clean(min_v, max_v)

            self.controller.df = cleaner.get_data()

            msg = f"Cleaning Complete | Rows: {len(self.controller.df)}"

            if self.remove_corr.get():
                msg += " | Correlated columns removed"

            self.status_label.configure(text=msg)

        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")

    def undo_changes(self):
        if self.controller.original_df is not None:
            self.controller.df = self.controller.original_df.copy()
            self.status_label.configure(
                text="Changes undone. Dataset reset to original.")
        else:
            self.status_label.configure(
                text="No original dataset to revert to.")

    def run_ai_clean(self):
        df = self.controller.df

        if df is None:
            self.status_label.configure(text="No dataset loaded")
            return

        try:
            analysis = analyze_data(df)

            print("\n=== AI Analysis ===")
            print(analysis)

            self.status_label.configure(text="Applying AI cleaning...")
            self.update_idletasks()

            cleaned_df = smart_clean(df)
            self.controller.df = cleaned_df

            self.status_label.configure(
                text=f"AI Cleaning Applied | Rows: {len(cleaned_df)}"
            )
        except Exception as e:
            self.status_label.configure(text=f"AI Error: {e}")

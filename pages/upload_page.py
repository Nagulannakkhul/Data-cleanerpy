import customtkinter as ctk
from components.step_indicator import StepIndicator
from tkinter import filedialog
import pandas as pd
import os
from utils import data_quality_report


class UploadPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Configure grid for flexibility
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # step indicator
        self.grid_rowconfigure(1, weight=1)  # main container

        # STEP INDICATOR
        step = StepIndicator(self, current_step=1)
        step.grid(row=0, column=0, sticky="ew", pady=(20, 20))

        # Main container
        container = ctk.CTkScrollableFrame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Configure container grid
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=0)  # title
        container.grid_rowconfigure(1, weight=0)  # subtitle
        container.grid_rowconfigure(2, weight=0)  # upload box
        container.grid_rowconfigure(3, weight=0)  # file label
        container.grid_rowconfigure(4, weight=0)  # info card
        container.grid_rowconfigure(5, weight=0)  # quality button
        container.grid_rowconfigure(6, weight=0)  # nav

        # Title
        title = ctk.CTkLabel(
            container,
            text="Upload Dataset",
            font=("Arial", 28, "bold")
        )
        title.grid(row=0, column=0, sticky="ew", pady=(30, 15))

        subtitle = ctk.CTkLabel(
            container,
            text="Supported formats: CSV, Excel (.xlsx)",
            font=("Arial", 12)
        )
        subtitle.grid(row=1, column=0, sticky="ew", pady=(0, 30))

        # Upload box
        self.upload_box = ctk.CTkFrame(
            container,
            corner_radius=15
        )
        self.upload_box.grid(row=2, column=0, sticky="ew", pady=15)
        self.upload_box.grid_columnconfigure(0, weight=1)
        self.upload_box.grid_rowconfigure(0, weight=1)  # label
        self.upload_box.grid_rowconfigure(1, weight=0)  # button

        upload_label = ctk.CTkLabel(
            self.upload_box,
            text="Click below to select a file",
            font=("Arial", 16)
        )
        upload_label.grid(row=0, column=0, sticky="nsew", pady=(40, 15))

        upload_btn = ctk.CTkButton(
            self.upload_box,
            text="Browse File",
            font=("Arial", 14),
            hover_color="#4444FF",  # Blue for action
            command=self.load_file
        )
        upload_btn.grid(row=1, column=0, sticky="ew", pady=(0, 40), padx=50)

        # File name
        self.file_label = ctk.CTkLabel(
            container,
            text="No file selected",
            font=("Arial", 14)
        )
        self.file_label.grid(row=3, column=0, sticky="ew", pady=(10, 20))

        # Dataset info card
        self.info_card = ctk.CTkFrame(container)
        self.info_card.grid(row=4, column=0, sticky="nsew", pady=(15, 15))
        self.info_card.grid_columnconfigure(0, weight=1)

        self.info_label = ctk.CTkLabel(
            self.info_card,
            text="Dataset info will appear here",
            font=("Arial", 12),
            wraplength=380
        )
        self.info_label.grid(row=0, column=0, sticky="nsew", pady=15, padx=10)

        # Data quality button
        quality_btn = ctk.CTkButton(
            container,
            text=" Data Info",
            font=("Arial", 12),
            hover_color="#4444FF",  # Blue for action
            command=lambda: controller.show_frame("QualityReportPage")
        )
        quality_btn.grid(row=5, column=0, sticky="ew", pady=(10, 25), padx=50)

        # Navigation
        nav_frame = ctk.CTkFrame(container, fg_color="transparent")
        nav_frame.grid(row=6, column=0, sticky="ew", pady=(15, 30))
        nav_frame.grid_columnconfigure(0, weight=1)

        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="Next →",
            font=("Arial", 14),
            state="disabled",
            hover_color="#44FF44",  # Green for next
            command=lambda: controller.show_frame("CleanPage")
        )
        self.next_btn.grid(row=0, column=0, sticky="ew", padx=20)

    # ------------------------
    # Load File
    # ------------------------

    def load_file(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx")
            ]
        )

        if not file_path:
            return

        try:

            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)

            else:
                df = pd.read_excel(file_path)

            self.controller.df = df
            self.controller.original_df = df.copy()
            self.controller.file_path = file_path

            filename = os.path.basename(file_path)
            rows, cols = df.shape

            self.file_label.configure(
                text=f"Selected file: {filename}"
            )

            self.info_label.configure(
                text=f"Rows: {rows}   |   Columns: {cols}"
            )

            self.next_btn.configure(state="normal")

        except Exception as e:
            self.info_label.configure(text=f"Error loading file: {e}")

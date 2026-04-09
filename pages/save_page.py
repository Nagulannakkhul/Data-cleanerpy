import customtkinter as ctk
from components.step_indicator import StepIndicator
from tkinter import filedialog
import pandas as pd


class SavePage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Configure grid for flexibility
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # step
        self.grid_rowconfigure(1, weight=0)  # title
        self.grid_rowconfigure(2, weight=0)  # preview label
        self.grid_rowconfigure(3, weight=1)  # preview box
        self.grid_rowconfigure(4, weight=0)  # preview btn
        self.grid_rowconfigure(5, weight=0)  # buttons
        self.grid_rowconfigure(6, weight=0)  # status

        # STEP INDICATOR
        step = StepIndicator(self, current_step=3)
        step.grid(row=0, column=0, sticky="ew", pady=(20, 20))

        title = ctk.CTkLabel(self, text="Save Cleaned Data",
                             font=("Arial", 24, "bold"))
        title.grid(row=1, column=0, sticky="ew", pady=(15, 25))

        preview_label = ctk.CTkLabel(
            self, text="Dataset Preview (first 5 rows)", font=("Arial", 14))
        preview_label.grid(row=2, column=0, sticky="ew", pady=(0, 15))

        # Textbox for preview
        self.preview_box = ctk.CTkTextbox(self, font=("Courier", 10))
        self.preview_box.grid(
            row=3, column=0, sticky="nsew", pady=(0, 15), padx=15)

        preview_btn = ctk.CTkButton(
            self,
            text="Refresh Preview",
            font=("Arial", 12),
            hover_color="#4444FF",  # Blue for action
            command=self.show_preview
        )
        preview_btn.grid(row=4, column=0, sticky="ew", pady=(10, 25), padx=200)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=5, column=0, sticky="ew", pady=(25, 30))

        back_btn = ctk.CTkButton(
            button_frame,
            text="Back",
            width=100,
            height=35,
            font=("Arial", 12),
            hover_color="red",
            command=lambda: controller.show_frame("CleanPage")
        )
        back_btn.grid(row=0, column=0, padx=15)

        save_btn = ctk.CTkButton(
            button_frame,
            text="Save File",
            width=100,
            height=35,
            font=("Arial", 12),
            hover_color="#4444FF",  # Blue for action
            command=self.save_file
        )
        save_btn.grid(row=0, column=4, padx=15)

        report_btn = ctk.CTkButton(
            button_frame,
            text="View Report",
            width=100,
            height=35,
            font=("Arial", 12),
            hover_color="#00AA88",
            command=self.open_report
        )

        report_btn.grid(row=0, column=3, pady=10, padx=20)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.grid(row=6, column=0, sticky="ew", pady=(10, 20))

    # ---------------------
    # Show Data Preview
    # ---------------------

    def show_preview(self):

        df = self.controller.df

        if df is None:
            self.preview_box.delete("0.0", "end")
            self.preview_box.insert("0.0", "No data available")
            return

        preview = df.head().to_string()

        self.preview_box.delete("0.0", "end")
        self.preview_box.insert("0.0", preview)

    # ---------------------
    # Save File
    # ---------------------

    def save_file(self):

        df = self.controller.df

        if df is None:
            self.status_label.configure(text="No dataset to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV File", "*.csv"),
                ("Excel File", "*.xlsx"),
                ("JSON File", "*.json")
            ]
        )

        if not file_path:
            return

        try:

            if file_path.endswith(".csv"):
                df.to_csv(file_path, index=False)

            elif file_path.endswith(".xlsx"):
                df.to_excel(file_path, index=False)

            elif file_path.endswith(".json"):
                df.to_json(file_path, orient='records')

            self.status_label.configure(text="File saved successfully")

        except Exception as e:
            self.status_label.configure(text=f"Error saving file: {e}")

    def open_report(self):
        self.controller.frames["ReportPage"].load_data()
        self.controller.show_frame("ReportPage")

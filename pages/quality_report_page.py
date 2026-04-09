import customtkinter as ctk
from components.step_indicator import StepIndicator
from utils import data_quality_report


class QualityReportPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Configure grid for flexibility
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # step
        self.grid_rowconfigure(1, weight=0)  # title
        self.grid_rowconfigure(2, weight=1)  # report box
        self.grid_rowconfigure(3, weight=0)  # back button

        # STEP INDICATOR (optional, or custom)
        step_label = ctk.CTkLabel(self, text="Data Quality Report", font=("Arial", 20, "bold"))
        step_label.grid(row=0, column=0, sticky="ew", pady=(20,10))

        title = ctk.CTkLabel(self, text="Dataset Quality Analysis", font=("Arial", 24, "bold"))
        title.grid(row=1, column=0, sticky="ew", pady=(10,20))

        # Report Textbox
        self.report_box = ctk.CTkTextbox(self, font=("Courier", 12), wrap="word")
        self.report_box.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0,20))

        # Back Button
        back_btn = ctk.CTkButton(
            self,
            text="Back to Upload",
            font=("Arial", 14),
            hover_color="red",
            command=lambda: controller.show_frame("UploadPage")
        )
        back_btn.grid(row=3, column=0, sticky="ew", pady=(10,30), padx=200)

        # Generate report on init
        self.refresh()

    def refresh(self):
        df = self.controller.df
        if df is None:
            report_text = "No dataset loaded."
        else:
            report = data_quality_report(df)
            report_text = f"""
Dataset Info:
  Rows: {report['dataset_info']['rows']}
  Columns: {report['dataset_info']['columns']}
  Column Names: {', '.join(report['dataset_info']['column_names'])}

Missing Values:
{chr(10).join([f"  {k}: {v}" for k, v in report['missing_values'].items()]) or "  None"}

Duplicate Rows: {report['duplicate_rows']}

Column Types:
{chr(10).join([f"  {k}: {v}" for k, v in report['column_types'].items()])}

Numeric Summary:
{chr(10).join([f"  {k}: {v}" for k, v in report['numeric_summary'].items()]) if report['numeric_summary'] else "  No numeric columns"}
"""

        self.report_box.configure(state="normal")
        self.report_box.delete("0.0", "end")
        self.report_box.insert("0.0", report_text.strip())
        self.report_box.configure(state="disabled")  # Make it read-only
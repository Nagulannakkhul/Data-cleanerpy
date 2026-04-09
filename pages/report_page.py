import customtkinter as ctk
from utils import advanced_quality_score, find_high_correlation


class ReportPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self, text="📊 Data Quality Report", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, pady=20)

        self.label = ctk.CTkLabel(
            self, text="", font=("Arial", 16), justify="left")
        self.label.grid(row=1, column=0, pady=20)

        back_btn = ctk.CTkButton(
            self,
            text="Back",
            command=lambda: controller.show_frame("CleanPage")
        )
        back_btn.grid(row=2, column=0, pady=20)

    def load_data(self):

        df = self.controller.df

        if df is None:
            self.label.configure(text="No data loaded")
            return

        report = advanced_quality_score(df)
        correlations = find_high_correlation(df)

        text = f"""
Data Quality Score: {report['score']}/100

Missing values: {report['missing']}%
Duplicates: {report['duplicates']}%
Empty cells: {report['empty']}%
Inconsistent text: {report['inconsistent']}%
Special characters: {report['special']}%
Negative values: {report['negative']}%
Outliers: {report['outliers']}%
Invalid dates: {report['invalid_dates']}%
"""
        corr_text = "\n".join(correlations) if correlations else "None"

        text += f"""

Highly Correlated Columns:
{corr_text}
"""

        self.label.configure(text=text)

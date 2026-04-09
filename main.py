import customtkinter as ctk

from pages.upload_page import UploadPage
from pages.clean_page import CleanPage
from pages.save_page import SavePage
from pages.quality_report_page import QualityReportPage
from pages.report_page import ReportPage


class DataCleanerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Excel / CSV Data Cleaner")
        self.geometry("600x700")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # shared data
        self.df = None
        self.original_df = None
        self.file_path = None

        # container for pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # register pages
        for Page in (UploadPage, CleanPage, SavePage, QualityReportPage, ReportPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("UploadPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, 'refresh'):
            frame.refresh()
        frame.tkraise()


if __name__ == "__main__":
    app = DataCleanerApp()
    app.mainloop()

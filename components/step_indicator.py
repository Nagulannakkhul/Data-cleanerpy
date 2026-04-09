import customtkinter as ctk


class StepIndicator(ctk.CTkFrame):

    def __init__(self, parent, current_step=1):
        super().__init__(parent)

        self.current_step = current_step

        self.steps = ["Upload", "Clean", "Save"]

        # Configure grid for flexibility
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)

        self.build_ui()

    def build_ui(self):

        for i, step in enumerate(self.steps, start=1):

            if i == self.current_step:
                color = "#3B8ED0"  # active
                text_color = "white"
            else:
                color = "#2B2B2B"
                text_color = "gray"

            step_box = ctk.CTkLabel(
                self,
                text=f"{step}",
                height=35,
                fg_color=color,
                text_color=text_color,
                corner_radius=8,
                font=("Arial", 12, "bold")
            )

            step_box.grid(row=0, column=(i-1)*2, sticky="ew", padx=8)

            # connector line
            if i < len(self.steps):
                line = ctk.CTkLabel(
                    self,
                    text="────",
                    text_color="gray",
                    font=("Arial", 14)
                )
                line.grid(row=0, column=(i-1)*2 + 1)
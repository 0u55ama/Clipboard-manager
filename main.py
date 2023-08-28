import customtkinter
import pyperclip


class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, **kwargs):
        super().__init__(master, **kwargs)

        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        checkbox.grid(row=len(self.checkbox_list), column=0, sticky="w", padx=10)
        checkbox.bind("<Button-1>", lambda event, text=item: self.copy_to_clipboard(text))
        self.checkbox_list.append(checkbox)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

    def add_copied_item(self, text):
        if text not in [checkbox.cget("text") for checkbox in self.checkbox_list]:
            self.add_item(text)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clipboard Manager")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200,
                                                                 item_list=[f"item {i}" for i in range(0)])
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.monitor_clipboard()

    def monitor_clipboard(self):
        last_copied_text = pyperclip.paste()
        self.after(1000, self.check_clipboard, last_copied_text)

    def check_clipboard(self, last_copied_text):
        current_copied_text = pyperclip.paste()
        if current_copied_text != last_copied_text:
            self.scrollable_checkbox_frame.add_copied_item(current_copied_text)
        self.monitor_clipboard()

    def checkbox_frame_event(self):
        selected_item = self.scrollable_checkbox_frame.get_checked_items()
        if selected_item:
            pyperclip.copy(selected_item[0])


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()

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
        checkbox.grid(row=len(self.checkbox_list), column=0, sticky="w", padx=10, pady=5)
        checkbox.bind("<Button-1>", lambda event, text=item: self.copy_to_clipboard(text))
        self.checkbox_list.append(checkbox)

    def copy_to_clipboard(self, text):
        stripped_text = text.strip()
        pyperclip.copy(stripped_text)

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

    def remove_selected_items(self):
        selected_items = self.get_checked_items()
        for checkbox in self.checkbox_list[:]:
            if checkbox.cget("text") in selected_items:
                self.remove_item(checkbox.cget("text"))

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def add_copied_item(self, text):
        if text not in [checkbox.cget("text") for checkbox in self.checkbox_list]:
            self.add_item(text)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clipboard Manager")
        self.grid_rowconfigure(0, weight=1)
        self.geometry("450x300")
        self.is_always_on_top = False
        self.resizable(False, False)  # Disable window resizing

        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=400,
                                                                 item_list=[f"item {i}" for i in range(0)])
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.monitor_clipboard()
        self.delete_button = customtkinter.CTkButton(self, text="Delete Selected Items", command=self.delete_selected_items,fg_color="#AD0000", hover_color="#AD0000")
        self.delete_button.grid(row=1, column=0, padx=15, pady=5, sticky="w")


        self.toggle_top_button = customtkinter.CTkButton(self, text="Toggle Always On Top", command=self.toggle_always_on_top)
        self.toggle_top_button.grid(row=2, column=0, padx=15, pady=5, sticky="w")

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

    def delete_selected_items(self):
        self.scrollable_checkbox_frame.remove_selected_items()

    def toggle_always_on_top(self):
        self.is_always_on_top = not self.is_always_on_top
        self.wm_attributes("-topmost", self.is_always_on_top)
        if self.is_always_on_top:
            toggle_text = "Toggle Always Off Top"
        else:
            toggle_text = "Toggle Always On Top"
        self.toggle_top_button.configure(text=toggle_text)




if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()

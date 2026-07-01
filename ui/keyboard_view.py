import customtkinter as ctk

class KeyboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.keys = {}
        self.layout = [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "BACKSPACE"],
            ["TAB", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["CAPS", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "ENTER"],
            ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "SHIFT"],
            ["SPACE"]
        ]

        self._build_keyboard()

    def _build_keyboard(self):
        for row in self.layout:
            row_frame = ctk.CTkFrame(self, fg_color="transparent")
            row_frame.pack(pady=2)

            for key in row:
                width = 45
                if key == "SPACE":
                    width = 320
                elif len(key) > 1:
                    width = 85

                btn = ctk.CTkButton(
                    row_frame,
                    text=key,
                    width=width,
                    height=40,
                    corner_radius=6,
                    fg_color="#333333",
                    text_color="white",
                    font=("Courier New", 12, "bold"),
                    state="disabled"
                )
                btn.pack(side="left", padx=2)
                self.keys[key] = btn

    def highlight_key(self, key_name: str, pressed: bool):
        key_name = key_name.upper()

        if key_name in ["SPACE", " "]:
            key_name = "SPACE"
        elif key_name in ["RETURN", "ENTER"]:
            key_name = "ENTER"
        elif key_name in ["BACKSPACE", "DELETE"]:
            key_name = "BACKSPACE"
        elif key_name in ["TAB"]:
            key_name = "TAB"
        elif key_name.startswith("SHIFT"):
            key_name = "SHIFT"
        elif key_name.startswith("CAPS"):
            key_name = "CAPS"

        if key_name in self.keys:
            btn = self.keys[key_name]
            if pressed:
                btn.configure(fg_color="#007acc")
            else:
                btn.configure(fg_color="#333333")

    def reset_highlights(self):
        for btn in self.keys.values():
            btn.configure(fg_color="#333333")

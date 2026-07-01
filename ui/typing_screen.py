import customtkinter as ctk
from core.typing_engine import TypingEngine
from ui.keyboard_view import KeyboardView

class TypingScreen(ctk.CTkFrame):
    def __init__(self, master, on_finish=None, on_back=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_finish = on_finish
        self.on_back = on_back
        self.engine = TypingEngine()
        self.lesson_info = None

        self._build_ui()
        self._bind_events()
        self.after(500, self._update_stats)

    def _build_ui(self):
        # Top bar
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=10, padx=20)

        self.back_btn = ctk.CTkButton(top, text="← Back", width=80, command=self._go_back)
        self.back_btn.pack(side="left")

        self.stats_label = ctk.CTkLabel(top, text="WPM: 0 | Accuracy: 100%", 
                                       font=("Courier New", 16, "bold"))
        self.stats_label.pack(side="right")

        # Lesson info
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=20, pady=5)

        self.title_label = ctk.CTkLabel(self.info_frame, text="", 
                                       font=("Courier New", 18, "bold"))
        self.title_label.pack(anchor="w")

        self.desc_label = ctk.CTkLabel(self.info_frame, text="", 
                                      font=("Courier New", 12))
        self.desc_label.pack(anchor="w")

        # Text display
        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.text_display = ctk.CTkTextbox(self.text_frame, font=("Courier New", 18),
                                          wrap="word", state="disabled",
                                          fg_color="transparent")
        self.text_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Keyboard
        self.keyboard = KeyboardView(self)
        self.keyboard.pack(pady=10)

        # Results frame (hidden initially)
        self.results_frame = ctk.CTkFrame(self)
        self.result_title = ctk.CTkLabel(self.results_frame, text="Session Complete!",
                                          font=("Courier New", 24, "bold"))
        self.result_title.pack(pady=10)

        self.result_stats = ctk.CTkLabel(self.results_frame, text="",
                                        font=("Courier New", 16))
        self.result_stats.pack(pady=5)

        self.result_explanation = ctk.CTkTextbox(self.results_frame, font=("Courier New", 14),
                                                  wrap="word", height=150)
        self.result_explanation.pack(fill="x", padx=20, pady=10)

        self.restart_btn = ctk.CTkButton(self.results_frame, text="Restart",
                                        command=self._restart)
        self.restart_btn.pack(pady=10)

    def _bind_events(self):
        self.master.bind("<Key>", self._on_key_press)
        self.master.bind("<KeyRelease>", self._on_key_release)
        self.master.bind("<BackSpace>", self._on_backspace)

    def load_lesson(self, text: str, title: str = "", description: str = "", 
                   explanation: str = ""):
        self.lesson_info = {
            "title": title,
            "description": description,
            "explanation": explanation
        }
        self.title_label.configure(text=title)
        self.desc_label.configure(text=description)
        self.engine.load_text(text)
        self._render_text()

    def _render_text(self):
        self.text_display.configure(state="normal")
        self.text_display.delete("0.0", "end")

        target = self.engine.target_text
        current = self.engine.current_index
        error = self.engine.error_state

        for i, char in enumerate(target):
            if char == "\n":
                display_char = "\u21B5\n"
            else:
                display_char = char

            tag = "pending"
            if i < current:
                tag = "correct"
            elif i == current:
                tag = "error" if error else "current"

            self.text_display.insert("end", display_char, tag)

        self.text_display.configure(state="disabled")
        self._apply_tags()

    def _apply_tags(self):
        self.text_display.tag_config("correct", foreground="#4CAF50")
        self.text_display.tag_config("error", foreground="#f44336", 
                                     underline=True, underlinefg="#f44336")
        self.text_display.tag_config("current", foreground="#2196F3", 
                                     underline=True, underlinefg="#2196F3")
        self.text_display.tag_config("pending", foreground="#757575")

    def _on_key_press(self, event):
        if self.engine.is_finished:
            return

        char = event.char
        if not char:
            return

        self.keyboard.highlight_key(event.keysym, True)

        if char == "\r":
            char = "\n"

        self.engine.process_keystroke(char)
        self._render_text()

        if self.engine.is_finished:
            self._show_results()

    def _on_key_release(self, event):
        self.keyboard.highlight_key(event.keysym, False)

    def _on_backspace(self, event):
        self.engine.process_backspace()
        self._render_text()
        return "break"

    def _update_stats(self):
        if not self.engine.is_finished:
            wpm = self.engine.get_wpm()
            acc = self.engine.get_accuracy()
            self.stats_label.configure(text=f"WPM: {wpm} | Accuracy: {acc}%")
        self.after(500, self._update_stats)

    def _show_results(self):
        result = self.engine.get_result()
        if result and self.on_finish:
            self.on_finish(result.wpm, result.accuracy)

        self.text_frame.pack_forget()
        self.keyboard.pack_forget()
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)

        if result:
            self.result_stats.configure(
                text=f"WPM: {result.wpm} | Accuracy: {result.accuracy}%\n"
                     f"Keystrokes: {result.total_keystrokes} | Errors: {result.errors}"
            )

        if self.lesson_info and self.lesson_info["explanation"]:
            self.result_explanation.configure(state="normal")
            self.result_explanation.delete("0.0", "end")
            self.result_explanation.insert("0.0", self.lesson_info["explanation"])
            self.result_explanation.configure(state="disabled")

    def _restart(self):
        self.results_frame.pack_forget()
        self.text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.keyboard.pack(pady=10)
        if self.lesson_info:
            self.load_lesson(
                self.engine.target_text,
                self.lesson_info["title"],
                self.lesson_info["description"],
                self.lesson_info["explanation"]
            )

    def _go_back(self):
        if self.on_back:
            self.on_back()

import customtkinter as ctk
import random
from core.lesson_loader import LessonLoader
from core.stats_manager import StatsManager
from ui.typing_screen import TypingScreen

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Typing Tutor")
        self.geometry("1000x750")
        self.resizable(False, False)

        self.lesson_loader = LessonLoader()
        self.stats_manager = StatsManager()
        self.lessons = self.lesson_loader.load_all_lessons()
        self.current_screen = None

        self._build_menu()

    def _build_menu(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = ctk.CTkFrame(self)
        self.current_screen.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(self.current_screen, text="⌨️ Typing Tutor",
                            font=("Courier New", 36, "bold"))
        title.pack(pady=40)

        # Best stats
        best_wpm, best_acc = self.stats_manager.get_best_stats()
        stats_text = f"Best: {best_wpm} WPM | {best_acc}% Accuracy"
        stats_label = ctk.CTkLabel(self.current_screen, text=stats_text,
                                  font=("Courier New", 14))
        stats_label.pack(pady=10)

        # Mode buttons
        btn_frame = ctk.CTkFrame(self.current_screen, fg_color="transparent")
        btn_frame.pack(pady=30)

        freestyle_btn = ctk.CTkButton(btn_frame, text="Freestyle",
                                     width=250, height=50,
                                     font=("Courier New", 16, "bold"),
                                     command=self._start_freestyle)
        freestyle_btn.pack(pady=10)

        custom_btn = ctk.CTkButton(btn_frame, text="Custom Snippet",
                                  width=250, height=50,
                                  font=("Courier New", 16, "bold"),
                                  command=self._start_custom)
        custom_btn.pack(pady=10)

        lessons_btn = ctk.CTkButton(btn_frame, text="Java Lessons",
                                   width=250, height=50,
                                   font=("Courier New", 16, "bold"),
                                   command=self._show_lessons)
        lessons_btn.pack(pady=10)

        # Theme toggle
        theme_btn = ctk.CTkButton(self.current_screen, text="Toggle Theme",
                                 width=150, command=self._toggle_theme)
        theme_btn.pack(pady=20)

    def _start_freestyle(self):
        words = ["public", "class", "void", "main", "String", "int", 
                "boolean", "if", "else", "for", "while", "return", 
                "new", "import", "static", "final", "try", "catch"]
        text = " ".join(random.choices(words, k=30))
        self._start_typing(text, "Freestyle", "Practice typing Java keywords", "")

    def _start_custom(self):
        dialog = ctk.CTkInputDialog(text="Paste your text to practice:", 
                                   title="Custom Snippet")
        text = dialog.get_input()
        if text:
            self._start_typing(text, "Custom", "Your custom text", "")

    def _show_lessons(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = ctk.CTkFrame(self)
        self.current_screen.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.current_screen, text="📚 Java Lessons",
                            font=("Courier New", 28, "bold"))
        title.pack(pady=20)

        back_btn = ctk.CTkButton(self.current_screen, text="← Back",
                                width=80, command=self._build_menu)
        back_btn.pack(anchor="nw", padx=20, pady=10)

        scroll = ctk.CTkScrollableFrame(self.current_screen, width=800, height=500)
        scroll.pack(pady=10, padx=20)

        for i, lesson in enumerate(self.lessons):
            card = ctk.CTkFrame(scroll)
            card.pack(fill="x", pady=5, padx=10)

            num = ctk.CTkLabel(card, text=f"{i+1}.", 
                              font=("Courier New", 14, "bold"), width=30)
            num.pack(side="left", padx=10)

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=10)

            lt = ctk.CTkLabel(info, text=lesson.title,
                             font=("Courier New", 14, "bold"))
            lt.pack(anchor="w")

            ld = ctk.CTkLabel(info, text=lesson.description,
                             font=("Courier New", 11))
            ld.pack(anchor="w")

            start = ctk.CTkButton(card, text="Start", width=80,
                                 command=lambda l=lesson: self._start_lesson(l))
            start.pack(side="right", padx=10)

    def _start_lesson(self, lesson):
        self._start_typing(lesson.code, lesson.title, lesson.description, 
                          lesson.explanation)

    def _start_typing(self, text, title, description, explanation):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = TypingScreen(
            self,
            on_finish=self._on_session_finish,
            on_back=self._build_menu
        )
        self.current_screen.pack(fill="both", expand=True)
        self.current_screen.load_text(text, title, description, explanation)

    def _on_session_finish(self, wpm, accuracy):
        self.stats_manager.save_session(wpm, accuracy, "typing")

    def _toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)

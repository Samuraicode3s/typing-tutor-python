import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class SessionResult:
    wpm: int
    accuracy: int
    total_keystrokes: int
    correct_keystrokes: int
    errors: int
    elapsed_seconds: float

class TypingEngine:
    def __init__(self):
        self.target_text = ""
        self.current_index = 0
        self.has_error = False
        self.start_time = None
        self.finished = False
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.errors = 0

    def load_text(self, text: str):
        self.target_text = text.replace("\r\n", "\n")
        self.current_index = 0
        self.has_error = False
        self.start_time = None
        self.finished = False
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.errors = 0

    def process_keystroke(self, char: str) -> bool:
        if self.finished or not self.target_text:
            return False

        if self.start_time is None:
            self.start_time = time.time()

        if self.has_error:
            if char == "\b":
                self.has_error = False
            return False

        expected = self.target_text[self.current_index]

        if char == expected:
            self.correct_keystrokes += 1
            self.total_keystrokes += 1
            self.current_index += 1
            if self.current_index >= len(self.target_text):
                self.finished = True
            return True
        elif char != "\b":
            self.errors += 1
            self.total_keystrokes += 1
            self.has_error = True
            return False
        return False

    def process_backspace(self) -> bool:
        if self.has_error:
            self.has_error = False
            return True
        return False

    def get_wpm(self) -> int:
        if self.start_time is None or self.correct_keystrokes == 0:
            return 0
        elapsed = time.time() - self.start_time
        if elapsed <= 0:
            return 0
        minutes = elapsed / 60.0
        words = self.correct_keystrokes / 5.0
        return int(words / minutes)

    def get_accuracy(self) -> int:
        if self.total_keystrokes == 0:
            return 100
        return int((self.correct_keystrokes / self.total_keystrokes) * 100)

    def get_result(self) -> Optional[SessionResult]:
        if not self.finished or self.start_time is None:
            return None
        elapsed = time.time() - self.start_time
        return SessionResult(
            wpm=self.get_wpm(),
            accuracy=self.get_accuracy(),
            total_keystrokes=self.total_keystrokes,
            correct_keystrokes=self.correct_keystrokes,
            errors=self.errors,
            elapsed_seconds=elapsed
        )

    @property
    def is_finished(self) -> bool:
        return self.finished

    @property
    def error_state(self) -> bool:
        return self.has_error

import json
import os
from dataclasses import dataclass
from typing import List

@dataclass
class Lesson:
    title: str
    description: str
    code: str
    explanation: str

class LessonLoader:
    def __init__(self, lessons_dir: str = "lessons"):
        self.lessons_dir = lessons_dir

    def load_all_lessons(self) -> List[Lesson]:
        lessons = []
        for i in range(1, 11):
            filename = f"lesson_{i:02d}.json"
            filepath = os.path.join(self.lessons_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    lessons.append(Lesson(
                        title=data["title"],
                        description=data["description"],
                        code=data["code"],
                        explanation=data["explanation"]
                    ))
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load {filename}: {e}")
        return lessons

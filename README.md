# Python Typing Tutor

A desktop typing tutor built with Python and CustomTkinter.

## Features
- **3 Modes**: Freestyle, Custom Snippet, Java Lessons
- **On-Screen Keyboard**: Real-time visual feedback
- **Error Highlighting**: Green = correct, Red = wrong, must fix before continuing
- **Live Stats**: WPM and accuracy calculated in real-time
- **Dark/Light Theme**: Toggle anytime
- **Local Stats**: Best scores saved to JSON

## Quick Start

### Run the app
Double-click `RUN.bat` or run:
```bash
pip install -r requirements.txt
python main.py
```

### Build .exe
Double-click `BUILD.bat` or run:
```bash
pip install pyinstaller
python build.py
```

### Create zip
Double-click `ZIP.bat` or run:
```bash
python zip_project.py
```

## Project Structure
```
typing-tutor/
├── main.py              # Entry point
├── core/                # Pure Python logic (no GUI)
│   ├── typing_engine.py
│   ├── stats_manager.py
│   └── lesson_loader.py
├── ui/                  # CustomTkinter GUI
│   ├── main_app.py
│   ├── typing_screen.py
│   └── keyboard_view.py
├── lessons/             # 10 built-in Java lessons
├── assets/              # Icon placeholder
├── stats/               # Local JSON stats
├── build.py             # PyInstaller script
├── zip_project.py       # Zip creator
├── RUN.bat              # Run the app
├── BUILD.bat            # Build .exe
├── ZIP.bat              # Create zip
└── requirements.txt
```

@echo off
echo Installing dependencies (first time only)...
pip install -r requirements.txt
echo.
echo Starting Typing Tutor...
python main.py
pause

@echo off
echo Installing PyInstaller...
pip install pyinstaller
echo.
echo Building .exe...
python build.py
echo.
echo Done! Check the dist/ folder.
pause

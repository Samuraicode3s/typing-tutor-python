import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.py',
    '--name=TypingTutor',
    '--onefile',
    '--windowed',
    '--add-data=lessons;lessons',
    '--add-data=assets;assets',
    '--icon=assets/icon.ico',
    '--clean'
])

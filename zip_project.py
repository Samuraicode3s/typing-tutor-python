import zipfile
import os

def create_zip():
    project_name = "typing-tutor"
    zip_name = f"{project_name}.zip"

    exclude = {'stats', 'build', 'dist', '__pycache__', '.git', 'venv', 'typing-tutor.zip'}

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file == zip_name:
                    continue
                filepath = os.path.join(root, file)
                zf.write(filepath, os.path.relpath(filepath, '.'))

    print(f"Created: {zip_name}")

if __name__ == "__main__":
    create_zip()

import os
import json
import csv
import nbformat
from docx import Document
from PyPDF2 import PdfReader

def read_file(filepath):
    ext = filepath.lower().split('.')[-1]
    try:
        if ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()

        elif ext == 'json':
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.dumps(json.load(f), indent=2)

        elif ext == 'csv':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()

        elif ext == 'pdf':
            reader = PdfReader(filepath)
            return "\n".join([page.extract_text() or '' for page in reader.pages])

        elif ext == 'docx':
            doc = Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])

        elif ext == 'ipynb':
            with open(filepath, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
                cells = [cell['source'] for cell in nb.cells if cell['cell_type'] == 'code']
                return "\n\n".join(cells)

        else:
            return "Unsupported file type: " + ext
    except Exception as e:
        return f"❌ Error reading file: {e}"

def list_files():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return "\n".join(files) if files else "No files found."

def mini_file_ai():
    print("🤖 MiniAI FileBot: Type 'list' to view files, 'read filename.ext', or 'bye' to exit.")
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'bye':
            print("MiniAI: Goodbye! 👋")
            break
        elif user_input.lower() == 'list':
            print("📂 Files in current folder:\n" + list_files())
        elif user_input.lower().startswith('read '):
            filename = user_input[5:].strip()
            if os.path.exists(filename):
                content = read_file(filename)
                print(f"\n📖 Content of {filename}:\n")
                print(content[:3000])  # Limit to 3000 chars
            else:
                print("❌ File not found.")
        else:
            print("MiniAI: I can only 'list', 'read filename', or 'bye'.")

# Run the AI
if __name__ == "__main__":
    mini_file_ai()
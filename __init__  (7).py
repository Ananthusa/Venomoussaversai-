(acess gemini api)
(sai uses the same logics )
(stimulate the the reality)
..........................

import os
import json
import yaml
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

        elif ext == 'yaml' or ext == 'yml':
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

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
            return "❌ Unsupported file type: " + ext
    except Exception as e:
        return f"❌ Error reading file '{filepath}': {e}"

def scan_drive_and_read_all(root_folder):
    print(f"🔍 Scanning folder: {root_folder}")
    for root, _, files in os.walk(root_folder):
        for file in files:
            filepath = os.path.join(root, file)
            print(f"\n📁 Reading: {filepath}")
            content = read_file(filepath)
            if isinstance(content, dict):
                print(json.dumps(content, indent=2))
            else:
                print(str(content)[:3000])  # Limit output
            print("-" * 60)

# Example: Use your own Drive path
drive_path = '/content/drive/MyDrive/ai_data'  # ← change to your folder
scan_drive_and_read_all(drive_path)
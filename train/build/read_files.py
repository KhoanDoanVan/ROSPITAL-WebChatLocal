import docx
import os

DOCS_FOLDER = os.path.join(os.path.dirname(__file__), "../docs")


def read_docs(file_name):
    file_path = os.path.join(DOCS_FOLDER, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    doc = docx.Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    return text
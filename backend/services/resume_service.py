import PyPDF2
import os

def extract_text_from_pdf(file_path):
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                text += page.extract_text() + "\n"

        return text.strip()

    except Exception as e:
        print("❌ Resume Parsing Error:", e)
        return ""
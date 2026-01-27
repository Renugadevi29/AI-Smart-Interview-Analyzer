import PyPDF2

def extract_resume_text(file_path: str) -> str:
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print("Resume parsing error:", e)

    return text.strip()

import pdfplumber
import tempfile
import os

async def extract_text_from_file(file):
    try:
        contents = await file.read()  # read first
        suffix = os.path.splitext(file.filename)[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        text = ""
        if suffix == ".pdf":
            with pdfplumber.open(tmp_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    print(f"Page {i+1}:", page_text[:200] if page_text else "No text extracted")
                    text += page_text or ""

        os.remove(tmp_path)
        return text.strip() if text.strip() else None

    except Exception as e:
        print(f"Error while extracting text: {e}")
        return None

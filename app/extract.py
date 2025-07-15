import os
import fitz  # PyMuPDF
import pdfplumber
import pdfminer.high_level
import io
import json


def extract_all_from_pdf(pdf_path: str) -> dict:
    result = {
        "filename": pdf_path,
        **extract_text(pdf_path),
        **extract_images_count(pdf_path),
        **extract_tables(pdf_path)
    }
    return result
def is_scanned_pdf(pdf_path: str) -> bool:
    # Скан или нет — по наличию текста
    import fitz
    doc = fitz.open(pdf_path)
    return all(not page.get_text().strip() for page in doc)


def extract_text(path: str) -> dict:
    try:
        text = pdfminer.high_level.extract_text(path)
        return {"text": text.strip()}
    except Exception as e:
        return {"text": '', "error": str(e)}


def extract_images_count(path: str) -> dict:
    try:
        doc = fitz.open(path)
        image_count = 0
        for page in doc:
            images = page.get_images(full=True)
            image_count += len(images)
        return {"image_count": image_count}
    except Exception as e:
        return {"image_count": '', "error": str(e)}


def extract_tables(path: str) -> dict:
    tables = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables.extend(page.extract_tables())
        return tables
    except Exception as e:
        return {"image_count": '', "error": str(e)}

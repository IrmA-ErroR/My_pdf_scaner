import os
import mimetypes

def is_valid_pdf(file_path: str) -> bool:
    """Проверяет, существует ли файл и является ли он PDF."""
    if not os.path.isfile(file_path):
        return False
    if not file_path.lower().endswith('.pdf'):
        return False

    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type == 'application/pdf'


def is_valid_pdf_folder(folder_path: str) -> bool:
    """Проверяет, существует ли папка и содержит ли хотя бы один PDF-файл."""
    if not os.path.isdir(folder_path):
        return False

    # pdf_files = [
    #     f for f in os.listdir(folder_path)
    #     if is_valid_pdf(os.path.join(folder_path, f))
    # ]
    # return len(pdf_files) > 0

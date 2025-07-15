import os
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from extract import extract_all_from_pdf


def process_and_save(pdf_path, output_dir):
    try:
        result = extract_all_from_pdf(pdf_path)
        name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(output_dir, f"{name}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return f"{name}.json saved"
    except Exception as e:
        return f"Failed to process {pdf_path}: {e}"


def process_pdf_folder(pdf_folder: str, output_dir: str, max_workers: int = None):
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = [
        os.path.join(pdf_folder, f)
        for f in os.listdir(pdf_folder)
        if f.lower().endswith(".pdf")
    ]

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_and_save, path, output_dir) for path in pdf_files]
        for future in as_completed(futures):
            result = future.result()
            print(result)
            results.append(result)

    return results

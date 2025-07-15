from flask import Flask, request, render_template
import os, shutil
from app import extract

# Абсолютный путь к текущей директории
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Путь до папки templates
TEMPLATES_DIR = os.path.join(BASE_DIR, "web", "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("pdf_file")
        folder = request.form.get("pdf_folder")
        output = request.form.get("output_dir")
        os.makedirs(output, exist_ok=True)

        paths = []
        if file:
            path = os.path.join("uploads", file.filename)
            file.save(path)
            paths = [path]
        elif folder:
            paths = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".pdf")]

        for pdf_path in paths:
            name = os.path.splitext(os.path.basename(pdf_path))[0]
            out_path = os.path.join(output, name)
            os.makedirs(out_path, exist_ok=True)

            # Извлекаем
            text = extract.extract_text_from_pdf(pdf_path)
            with open(os.path.join(out_path, "text.txt"), "w", encoding="utf-8") as f:
                f.write(text)

            tables = extract.extract_tables(pdf_path)
            for idx, table in enumerate(tables):
                with open(os.path.join(out_path, f"table_{idx}.csv"), "w", encoding="utf-8") as f:
                    for row in table:
                        f.write(",".join(row) + "\n")

            extract.extract_images_from_pdf(pdf_path, out_path)

        return "Обработка завершена!"
    return render_template("index.html")


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)

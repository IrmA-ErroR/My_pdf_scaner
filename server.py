import os
import json
from flask import Flask, request, render_template
import app
from app.extract import extract_all_from_pdf
# from app.runner import process_pdf_folder

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
            filename = file.filename
            path = os.path.join("uploads", filename)
            file.save(path)
            name = os.path.splitext(filename)[0]
            out_path = os.path.join(output, f"{name}.json")
            result = extract_all_from_pdf(path)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

        elif folder and os.path.isdir(path):
            app.runner.process_pdf_folder(folder, output, max_workers=os.cpu_count())

        return "Обработка завершена!"
    return render_template("index.html")


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)

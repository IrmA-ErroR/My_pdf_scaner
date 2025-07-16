import os
import json
from flask import Flask, request, render_template
from app import extractor, runner
# from app.extract import extract_all_from_pdf
# from app.runner import process_pdf_folder
import config

pdf_app = Flask(__name__, template_folder=config.TEMPLATES_DIR)

@pdf_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("pdf_file")
        folder = request.form.get("pdf_folder")
        output = request.form.get("output_dir")
        if not output:
            output = config.DEFAULT_OUTPUT_DIR
        os.makedirs(output, exist_ok=True)

        if file:
            filename = file.filename
            path = os.path.join(config.UPLOADS_DIR, filename)
            file.save(path)
            name = os.path.splitext(filename)[0]
            out_path = os.path.join(output, f"{name}.json")
            result = extractor.extract_all_from_pdf(path)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

        elif folder and os.path.isdir(folder):
            runner.process_pdf_folder(folder, output, max_workers=os.cpu_count())

        return "Обработка завершена!"
    return render_template("index.html", default_output_dir=config.DEFAULT_OUTPUT_DIR)


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    pdf_app.run(debug=True)

import os

# Абсолютный путь к текущей директории
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, "web", "templates")
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

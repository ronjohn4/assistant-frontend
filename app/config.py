"""Application configuration."""
import os
from pathlib import Path


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY")

    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", 0)
    PORT = os.environ.get("PORT", 5002)
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT", "true")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
    UPLOAD_FOLDER = Path(os.environ.get("UPLOAD_FOLDER", "uploads")).resolve()
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS", '{"png", "jpg", "jpeg", "gif", "webp"}')
    MAX_HISTORY_TURNS = int(os.environ.get("MAX_HISTORY_TURNS", 20))
    CHATBOT_NAME = os.environ.get("CHATBOT_NAME", "Riko")
    AGENT_URL = os.environ.get("AGENT_URL", "http://localhost:5010")


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in Config.ALLOWED_EXTENSIONS


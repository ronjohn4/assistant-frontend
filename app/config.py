"""Application configuration."""
import os
from pathlib import Path


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY")

    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
    PORT = os.environ.get("PORT")
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT").lower() == "true"
    LOG_LEVEL = os.environ.get("LOG_LEVEL")
    UPLOAD_FOLDER = Path(os.environ.get("UPLOAD_FOLDER")).resolve()
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS")
    MAX_HISTORY_TURNS = int(os.environ.get("MAX_HISTORY_TURNS"))
    CHATBOT_NAME = os.environ.get("CHATBOT_NAME")
    AGENT_URL = os.environ.get("AGENT_URL")


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in Config.ALLOWED_EXTENSIONS


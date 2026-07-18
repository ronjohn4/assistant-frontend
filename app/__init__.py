"""Flask application factory."""
from pathlib import Path
from flask import Flask
from flask_htmx import HTMX
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from app.config import Config


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    # Ensure upload directory exists
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    @app.context_processor
    def inject_chatbot_name():
        return {"chatbot_name": app.config["CHATBOT_NAME"]}

    HTMX(app)

    from app.routes import chat
    app.register_blueprint(chat.bp)

    app.logger.handlers = []  # remove the default logger to StreamHandler()
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/assistant-frontend.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(file_handler)

    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.info('Assistant frontend startup')

    return app

app = create_app()

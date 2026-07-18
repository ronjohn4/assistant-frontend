import threading
import uuid
from pathlib import Path
from flask import Blueprint, current_app, make_response as flask_make_response, \
        render_template, request, send_from_directory
from flask_htmx import make_response
from werkzeug.utils import secure_filename
import requests
import strip_markdown
from unidecode import unidecode

from app.config import Config
from app.config import allowed_file
from app.utilities.say import speak
import re

bp = Blueprint("chat", __name__)

def _save_upload(file) -> str | None:
    """Save uploaded image; return stored filename (for URL) or None."""
    current_app.logger.debug(f"_save_upload() start")

    if not file or file.filename == "":
        return None
    if not allowed_file(file.filename):
        return None
    name = secure_filename(file.filename)
    stem = uuid.uuid4().hex[:12]
    ext = Path(name).suffix.lower()
    stored = f"{stem}{ext}"
    folder = Path(current_app.config["UPLOAD_FOLDER"])
    path = folder / stored
    file.save(path)
    return stored


def _process_message(request_text: str | None, image_filename: str | None) -> str:
    """Process user input with conversational context."""
    current_app.logger.debug(f"_process_message() start")

    if request_text and request_text.strip():
        payload = {
            "query": request_text,
            "query-path": None,
            "response" : None,
            "response-path": None,  
        }
        current_app.logger.debug(f"_process_message(payload): {payload}")
        current_app.logger.debug(f'_process_message(AGENT_URL): {current_app.config["AGENT_URL"]}/agent')        
        
        response = requests.post(f'{current_app.config["AGENT_URL"]}/agent', json=payload)
        current_app.logger.debug(f"_process_message() after request.post()")
        current_app.logger.debug(f"_process_message(): {response}")

        if response.status_code == 200:
            # models return markdown, convert to html for display
            returned_text = strip_markdown.strip_markdown(response.text)
            returned_text = returned_text.strip()

            clean_unicode_text = unidecode(returned_text)
            clean_escape_text = clean_unicode_text.encode('utf-8').decode('unicode_escape') 

            return clean_escape_text
        else:
            current_app.logger.error(f"_process_message(): {response.status_code}")
            return "An error occurred while processing your message."
        
    if image_filename:
        return "Not sure what to do with an image."
    return "Send a message or an image to get a reply."


@bp.route("/uploads/<path:filename>") 
def uploads(filename: str):
    """Serve uploaded images."""
    current_app.logger.debug(f"upload() start")
    folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(str(folder), filename)


@bp.route("/")
def index():
    current_app.logger.debug(f"index() start")
    return render_template(
        "index.html",
        chatbot_name=current_app.config["CHATBOT_NAME"],
    )


@bp.route("/message", methods=["POST"])
def message():
    current_app.logger.debug(f"message() start")
    text = request.form.get("message", "").strip() or None
    image = request.files.get("image")
    image_filename = _save_upload(image) if image else None
    current_app.logger.debug(f"message() done retrieving parameters")

    if not text and not image_filename:
        if request.headers.get("HX-Request"):
            r = flask_make_response(
                render_template(
                    "partials/error.html",
                    error="Please enter a message or attach an image.",
                ),
                400,
            )
            r.headers["HX-Retarget"] = "#form-errors"
            r.headers["HX-Reswap"] = "innerHTML"
            return r

        return "Bad Request", 400

    current_app.logger.debug(f"message() ready to _process_message()")

    reply = _process_message(text, image_filename)

    current_app.logger.debug(f"message() done _process_message()")

    # TODO - The reply may be long and have bulleted lists.
    # It should ask if the deeper response should be spoken.
    # TODO - need to terminate the say() processing if another say() action takes place.

    parts = re.split(r'(?<=[.!?])\s+', reply, maxsplit=1)
    first_sentence = parts[0]

    if first_sentence != reply:
        first_sentence = first_sentence + "  Shortened."
    threading.Thread(target=speak, args=(first_sentence,), daemon=True).start()

    current_app.logger.debug(f"message() done with speak")

    if request.headers.get("HX-Request"):
        resp = make_response(
            render_template(
                "partials/bot_message.html",
                bot_message=reply,
                chatbot_name=current_app.config["CHATBOT_NAME"],
            )
        )

        current_app.logger.debug(f"message() done with make_response()")

        resp.headers["HX-Retarget"] = "#msg-loading"
        resp.headers["HX-Reswap"] = "outerHTML"
        resp.headers["HX-Trigger-After-Swap"] = "focus-input"
        return resp

    return "OK", 200


@bp.route("/say", methods=["POST"])
def say_test():
    current_app.logger.debug(f"message() say")
    try:
        threading.Thread(target=speak, args=("Test 1,2,3",), daemon=True).start()
    except Exception as e:
        current_app.logger.debug(f"message() say Exception 1")

    return "OK", 200
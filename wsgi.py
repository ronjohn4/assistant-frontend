"""Run the Flask chatbot app with Waitress."""
import os
from dotenv import load_dotenv
from waitress import serve

load_dotenv()

from app import app


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5002))

    try:
        serve(app, host=host, port=port)
    except OSError as exc:
        raise RuntimeError(f"Unable to start Waitress on {host}:{port}: {exc}") from exc


if __name__ == "__main__":
    main()
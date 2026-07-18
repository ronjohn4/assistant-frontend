"""Run the Flask chatbot app."""
import os

from dotenv import load_dotenv
load_dotenv()

from app import app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")

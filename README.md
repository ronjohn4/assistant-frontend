# Agent Frontend

This project provides a small Flask web chat interface for talking to an agent backend. It renders a browser-based chat UI, accepts text messages and image uploads, forwards user messages to an upstream agent endpoint, and displays the returned response in the page.

## What it does

- Presents a simple chat experience in the browser
- Sends user messages to an agent service at the configured AGENT_URL
- Supports optional image uploads (currently saved to the upload folder, but image handling is limited)
- Uses HTMX for dynamic message updates without full page reloads

## Requirements

- Python 3.10+
- A running agent backend that exposes an endpoint at /agent

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables if needed. The app uses the following defaults:
   - PORT: 5001
   - FLASK_DEBUG: 0
   - SECRET_KEY: dev-secret-change-in-production
   - UPLOAD_FOLDER: uploads
   - CHATBOT_NAME: Riko
   - AGENT_URL: http://localhost:5010

   Example:
   ```bash
   set AGENT_URL=http://localhost:5010
   set CHATBOT_NAME=Riko
   set FLASK_DEBUG=1
   ```

## Run the app

```bash
python main.py
```

Then open http://localhost:5001 in your browser.

## How to use it

- Type a message in the chat box and press send
- The app sends the message to the configured agent backend and shows the reply in the conversation
- You can also attach an image, which is stored in the upload folder, but the current UI does not perform any special image processing

## Project structure

- main.py: starts the Flask application
- app/: Flask app package with routes, templates, static assets, and utilities
- uploads/: default folder for uploaded files

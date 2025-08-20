#!/usr/bin/env python3
import os
import json
import csv
import io
from pathlib import Path
from typing import Dict, Any, List

# --- New libraries needed ---
# pip install python-docx
import docx
from PyPDF2 import PdfReader

from dotenv import load_dotenv
from flask import Flask, render_template, request, Response, session, redirect, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import google.generativeai as genai

# ----------------------------- CONFIG ---------------------------------
# Load environment variables from .env file
load_dotenv()

# --- API Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")

# Set the key for all Google AI/ML libraries
os.environ["GOOGLE_API_KEY"] = API_KEY
genai.configure(api_key=API_KEY)

# --- Paths ---
BASE_DIR = Path(__file__).parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# --- Flask ---
app = Flask(__name__)
# A secret key is required for using the session feature
app.config['SECRET_KEY'] = os.urandom(24)

# --- Model & Prompt Configuration ---
LLM_MODEL = "gemini-1.5-flash"

# This prompt is engineered to instruct the AI to act as a specialist
# in parsing logistics documents and to return structured JSON data.
SOF_EXTRACTION_PROMPT = """
You are an expert AI assistant specializing in logistics and shipping documentation. Your task is to meticulously extract all port operations events from the provided 'Statement of Facts' (SoF) document text.

Follow these instructions carefully:
1.  **Identify all Events**: Scan the entire document text to find any mention of port activities, vessel operations, or cargo handling. Examples include 'Vessel arrived', 'Anchorage', 'Pilot on board', 'Commenced loading', 'Shifting berth', 'Bunkering', 'Cargo operations completed', etc.
2.  **Extract Timestamps**: For each event you identify, find its corresponding 'start_time' and 'end_time'. The times might be in various formats (e.g., '2024-08-20 14:30', '20/08/2024 1430 hrs', 'Aug 20, 2024, 2:30 PM'). Standardize them where possible.
3.  **Handle Missing Data**: If an event only has a single timestamp, treat it as the 'start_time' and set 'end_time' to null. If a time is unclear or not present for an event, set the respective field to null.
4.  **Format the Output**: Return the data as a single JSON object. This object must contain one key: "events". The value of "events" should be a list of individual event objects. Each object in the list must have three keys: "event", "start_time", and "end_time".
5.  **Be Comprehensive**: Do not miss any events. It is critical to extract every single operation listed in the document.

Example Output Format:
{
  "events": [
    {
      "event": "Vessel arrived at pilot station",
      "start_time": "2024-08-20 10:00",
      "end_time": null
    },
    {
      "event": "Cargo Loading Operation",
      "start_time": "2024-08-20 14:30",
      "end_time": "2024-08-21 02:00"
    }
  ]
}

Now, analyze the following SoF document text and provide the structured JSON output.
"""

# --------------------------- UTILITIES ---------------------------------

def allowed_file(filename: str) -> bool:
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_document_text(file_storage: FileStorage | None) -> str:
    """Extracts text content from an uploaded PDF or DOCX file."""
    if not file_storage or not file_storage.filename or not allowed_file(file_storage.filename):
        return ""

    text = ""
    try:
        filename = file_storage.filename.lower()
        if filename.endswith('.pdf'):
            pdf_reader = PdfReader(file_storage)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        elif filename.endswith('.docx'):
            doc = docx.Document(file_storage)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        print(f"Error reading document {file_storage.filename}: {e}")
        return ""
    return text


def extract_sof_data_from_text(sof_text: str) -> Dict[str, Any]:
    """Uses the Gemini model in JSON mode to extract events, start times, and end times."""
    if not sof_text.strip():
        return {"error": "Document text is empty or could not be read."}

    try:
        model = genai.GenerativeModel(
            LLM_MODEL,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        response = model.generate_content([SOF_EXTRACTION_PROMPT, f"DOCUMENT TEXT:\n{sof_text}"])
        return json.loads(response.text)
    except Exception as e:
        print(f"Error during AI data extraction: {e}")
        # Fallback for when the model fails to generate perfect JSON
        return {"error": f"Failed to extract structured data from the document. AI model error: {e}"}


# ------------------------------ FLASK ROUTES ---------------------------------

@app.get("/")
def index() -> str:
    """Renders the main page with the file upload form."""
    return render_template("index.html")


@app.post("/")
def upload_and_process_sof() -> str:
    """Processes the uploaded SoF document and displays the extracted data."""
    if 'sof_document' not in request.files:
        return redirect(request.url)

    file = request.files['sof_document']
    render_ctx = {"filename": file.filename}

    if file.filename == '':
        render_ctx["error"] = "No file selected. Please choose a PDF or Word document."
        return render_template("index.html", **render_ctx)

    if file and allowed_file(file.filename):
        # 1. Extract text from the uploaded document
        sof_text = get_document_text(file)
        if not sof_text:
            render_ctx["error"] = "Could not extract any text from the document. It might be empty, corrupted, or an image-based file."
            return render_template("result.html", **render_ctx)

        # 2. Use the AI model to extract structured data
        extracted_data = extract_sof_data_from_text(sof_text)

        # 3. Store data in session for downloading and render the results page
        if "error" in extracted_data:
            render_ctx["error"] = extracted_data["error"]
        else:
            session['sof_data'] = extracted_data.get("events", [])
            render_ctx['events'] = session['sof_data']

        return render_template("result.html", **render_ctx)
    else:
        render_ctx["error"] = "Invalid file type. Please upload a PDF (.pdf) or Word (.docx) file."
        return render_template("index.html", **render_ctx)


@app.get("/download/<filetype>")
def download_file(filetype: str):
    """Handles downloading the extracted data as JSON or CSV."""
    events = session.get('sof_data', [])
    if not events:
        return redirect(url_for('index'))

    if filetype == 'json':
        # Create a JSON response
        return Response(
            json.dumps({"events": events}, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": "attachment;filename=sof_events.json"}
        )
    elif filetype == 'csv':
        # Create a CSV response
        output = io.StringIO()
        if events:
            writer = csv.DictWriter(output, fieldnames=events[0].keys())
            writer.writeheader()
            writer.writerows(events)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=sof_events.csv"}
        )

    return redirect(url_for('index'))

# ------------------------------ MAIN -----------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
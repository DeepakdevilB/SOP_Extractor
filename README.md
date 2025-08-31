🚢 Maritime SoF Event Extractor

A web application that uses the Gemini AI model to automatically extract structured data from maritime Statement of Facts (SoF) documents.

Users can upload PDF or DOCX files, and the app will parse them to identify key vessel details and generate a chronological log of port operations events.

✨ Features

🤖 AI-Powered Extraction – Leverages Gemini AI to understand and parse complex, unstructured maritime documents.

🌐 Web-Based Interface – User-friendly interface for uploading documents and viewing results.

📄 Handles Multiple File Types – Supports both digital text-based and scanned (image-based) PDFs and DOCX files.

📊 Structured Data Output – Converts unstructured SoF text into a clean JSON object containing ship details and event timelines.

🔍 Event Analysis – Quick insights on extraction: success rate, parsed vs. skipped events.

📥 Data Export – Download results as JSON (full data) or CSV (event log only).

🛠️ Tech Stack

Backend: Python, Flask

AI Model: Google Gemini (via google-generativeai library)

Frontend: HTML, CSS, JavaScript (Flask templates)

⚙️ Setup & Installation
1️⃣ Prerequisites

Python 3.8+

A Gemini API Key (Get one from Google AI Studio
)

2️⃣ Clone the Repository
git clone <your-repository-url>
cd <your-repository-directory>

3️⃣ Create a Virtual Environment
# Create venv
python3 -m venv venv  

# Activate (Linux / macOS)
source venv/bin/activate  

# Activate (Windows)
.\venv\Scripts\activate  

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Configure Your API Key

Create a .env file in the root directory and add:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

🚀 Running the Application

With your venv activated and .env configured, start the server:

python3 app.py


The app will be available at:
👉 http://127.0.0.1:8081

📖 How to Use

Open Web App → Go to http://127.0.0.1:8081

Upload Document → Drag & drop or browse a PDF/DOCX file

Select Processing Type

🖼️ Scanned / Image Document → Uses OCR

✍️ Digital Text Document → For selectable text PDFs/DOCX

Extract Events → Click "Set Sail & Extract"

View & Download

Vessel details + port event timeline displayed

Download results as JSON or CSV

📌 Example Output
{
  "vessel_name": "MV Georgia M",
  "voyage_no": "2025-08",
  "port": "Singapore",
  "events": [
    {"time": "2025-08-20 09:00", "event": "Pilot on board"},
    {"time": "2025-08-20 09:30", "event": "Vessel berthed"},
    {"time": "2025-08-20 10:00", "event": "Cargo operations commenced"}
  ]
}

📂 Data Export

JSON → Complete extracted vessel + event data

CSV → Only chronological event log

🤝 Contributing

Contributions are welcome! 🎉

Fork this repo

Create a new branch (feature-xyz)

Submit a PR

📜 License

This project is licensed under the MIT License.
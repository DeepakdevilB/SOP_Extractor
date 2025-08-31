Maritime SoF Event Extractor
This web application uses the Gemini AI model to automatically extract structured data from maritime "Statement of Facts" (SoF) documents. Users can upload PDF or DOCX files, and the application will parse them to identify key details like vessel information and a chronological log of port operations events.

The application is built with Python and Flask for the backend, and uses the google-generativeai library to interface with the Gemini API.

Features
AI-Powered Extraction: Leverages the Gemini model to understand and parse complex, unstructured maritime documents.

Web-Based Interface: A modern and user-friendly interface for uploading documents and viewing results.

Handles Multiple Document Types: Supports both text-based (digital) and scanned (image-based) PDF and DOCX files.

Structured Data Output: Converts unstructured SoF text into a clean JSON object containing ship details and a timeline of events.

Event Analysis: Provides a quick analysis of the extraction process, including success rate and the number of parsed vs. skipped events.

Data Export: Allows users to download the full extracted data as a JSON file or just the event log as a CSV file.

Setup and Installation
Follow these steps to set up and run the project locally.

1. Prerequisites
Python 3.8 or newer

A Gemini API Key. You can get one from Google AI Studio.

2. Clone the Repository
git clone <your-repository-url>
cd <your-repository-directory>

3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

# Create the virtual environment
python3 -m venv venv

# Activate it (on macOS/Linux)
source venv/bin/activate

# Activate it (on Windows)
.\venv\Scripts\activate

4. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

pip install -r requirements.txt

5. Configure Your API Key
The application loads your Gemini API key from a .env file.

Create a new file named .env in the root of your project directory.

Add your API key to this file as follows:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

How to Run
With your virtual environment activated and the .env file configured, start the Flask web server with the following command:

python3 app.py

The application will now be running and accessible at http://127.0.0.1:8081 in your web browser.

How to Use
Open the Web Interface: Navigate to http://127.0.0.1:8081.

Upload a Document: Drag and drop your SoF document (PDF or DOCX) into the upload area, or click to browse for a file.

Select Processing Type:

Choose "Scanned / Image Document" for files that are images or scans (requires OCR).

Choose "Digital Text Document" for files where the text is selectable.

Extract Events: Click the "Set Sail & Extract" button to process the document.

View and Download: The application will display the extracted vessel details and the timeline of port events. You can then download the complete data as a JSON file or the event list as a CSV file.
#SoF AI Extractor
A web-based application that uses Google's Gemini AI to automatically extract port operation events, start times, and end times from "Statement of Facts" (SoF) documents. The system accepts PDF and Word files, processes them in a template-agnostic way, and provides the structured data for download as JSON or CSV.📋 Table of ContentsFeaturesTech StackSetup and InstallationHow to RunHow to UseProject StructureFuture Improvements✨ FeaturesAI-Powered Extraction: Leverages the Google Gemini Flash model for intelligent and accurate data extraction.Multi-Format Support: Accepts both PDF (.pdf) and Word (.docx) documents.Template-Agnostic: Designed to work with various SoF layouts and formats without pre-configuration.Structured Output: Converts unstructured text into a clean, structured list of events.Data Download: Allows users to download the extracted data in both JSON and CSV formats.Modern UI: Clean, responsive, and user-friendly interface with a drag-and-drop file upload zone.🛠️ Tech StackBackend: Python 3Web Framework: FlaskAI Model: Google Gemini 1.5 FlashDocument Processing:PyPDF2 for PDF text extraction.python-docx for Word document text extraction.Frontend: HTML5, Bootstrap 5, Custom CSS & JavaScript🚀 Setup and InstallationFollow these steps to set up the project on your local machine.1. PrerequisitesPython 3.8 or newerA Google Gemini API Key. You can get one from Google AI Studio.2. Clone the RepositoryFirst, clone this repository to your local machine (or simply download and set up the folder structure as described below).git clone https://github.com/your-username/sof-ai-extractor.git
cd sof-ai-extractor
3. Install DependenciesIt's recommended to use a virtual environment to manage dependencies.# Create a virtual environment
python -m venv venv

## Activate the virtual environment
## On Windows:
venv\Scripts\activate
## On macOS/Linux:
source venv/bin/activate
Install the required Python packages using pip:pip install Flask google-generativeai python-dotenv PyPDF2 python-docx
4. Set Up Environment VariablesCreate a file named .env in the root of your project directory. This file will store your API key securely.Open the .env file and add your Gemini API key:GEMINI_API_KEY="YOUR_API_KEY_HERE"
▶️ How to RunWith the setup complete, you can now run the Flask web server.Make sure you are in the root directory of the project.Run the application using the following command:python app.py
The server will start, and you should see output similar to this: * Serving Flask app 'app'
 * Running on http://120.0.0.1:8081
Press CTRL+C to quit
Open your web browser and navigate to http://127.0.0.1:8081. How to UseOpen the Web Interface: Go to http://127.0.0.1:8081.Upload a Document: Drag and drop your SoF file (PDF or Word) onto the upload area, or click the area to browse and select a file from your computer.Extract Events: Click the "Extract Events" button. The application will send the document text to the Gemini API for processing.View Results: You will be redirected to a results page showing the extracted events in a clean table.Download Data: Click the "Download as JSON" or "Download as CSV" buttons to save the structured data to your computer.📁 Project StructureThe project follows a standard Flask application structure:sof-ai-extractor/
├── .env                  # Stores environment variables like the API key
├── app.py                # The main Flask application logic
└── templates/
    ├── index.html        # The main file upload page
    └── result.html       # The page to display extraction results
🔮 Future ImprovementsOCR Support: Integrate an OCR (Optical Character Recognition) library like Tesseract to handle scanned or image-based PDFs.Batch Processing: Allow users to upload and process multiple documents at once.Advanced Data Validation: Implement checks to validate the format of extracted dates and times.Database Integration: Store extraction results in a database (like SQLite or PostgreSQL) to keep a history of processed documents.User Authentication: Add a login system to manage access for different users.

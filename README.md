# Universal Credit Act Analyzer

## Overview

A Streamlit-based application for automated analysis of legislative documents. The system extracts text from PDF files, processes them through the Groq LLM, and generates structured JSON reports containing summaries, key sections, and compliance rule checks.

## Demo Video
[LINK](https://drive.google.com/file/d/15eOLKrFhvsZtaF-hIMHiBV1RgSluzQLX/view?usp=sharing)

## Tech Stack

### Core Technologies
- **Python 3.8+**: Programming language
- **Streamlit**: Web application framework for interactive UI
- **Groq LLM**: Large language model API for document analysis
- **Llama 3.1 70B**: Model used for text processing and analysis

### Libraries
- **pdfplumber**: PDF text extraction and parsing
- **groq**: Official Groq Python SDK for API calls
- **json**: Built-in library for JSON manipulation

### Dependencies
```
streamlit==1.28.1
groq==0.4.2
pdfplumber==0.10.3
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher installed
- Groq API key (free tier available at https://console.groq.com)

### Installation Steps

1. Clone the repository
```bash
git clone https://github.com/Bhudil/json_agent.git
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure API Key
Open `app.py` and replace the placeholder with your Groq API key:
```python
GROQ_API_KEY = "your_groq_api_key_here"
```

5. Run the application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## How It Works

### Architecture Overview

The application follows a linear pipeline architecture:

```
PDF Upload → Text Extraction → LLM Analysis → JSON Output
```

### Process Flow

#### 1. PDF Upload
- User uploads a PDF document via the Streamlit sidebar file uploader
- File is temporarily stored in memory for processing

#### 2. Text Extraction (Task 1)
- `extract_pdf_text()` function processes the PDF
- Uses pdfplumber to extract text from all pages
- Returns clean, concatenated text string
- Handles extraction errors gracefully

#### 3. Document Analysis (Tasks 2-4)
- Extracted text is sent to Groq API with a structured prompt
- Llama 3.1 70B model processes the document
- Single API call performs all analysis tasks simultaneously:

**Task 2 - Summarization**
- Generates 5-10 bullet points
- Focuses on: Purpose, Key Definitions, Eligibility, Obligations, Enforcement

**Task 3 - Section Extraction**
- Extracts 7 key legislative sections:
  - Definitions
  - Obligations
  - Responsibilities
  - Eligibility
  - Payments/Entitlements
  - Penalties/Enforcement
  - Record-keeping/Reporting

**Task 4 - Rule Compliance Checks**
- Validates 6 legislative requirements:
  1. Act must define key terms
  2. Act must specify eligibility criteria
  3. Act must specify responsibilities of administering authority
  4. Act must include enforcement or penalties
  5. Act must include payment calculation or entitlement structure
  6. Act must include record-keeping or reporting requirements

- For each rule, provides:
  - Pass/Fail status
  - Evidence from the document
  - Confidence score (0-100)

#### 4. Response Parsing
- LLM response is parsed to extract JSON
- JSON validation ensures structural integrity
- Results stored in Streamlit session state

#### 5. Display and Download
- Results displayed in formatted UI sections
- Summary as numbered bullet points
- Sections displayed in 2-column layout
- Rule checks with status, evidence, and confidence metrics
- Full JSON report available in expandable view
- Download button generates timestamped JSON file

### JSON Output Format

```json
{
  "summary": [
    "Bullet point 1",
    "Bullet point 2",
    "Bullet point 3",
    "Bullet point 4",
    "Bullet point 5"
  ],
  "sections": {
    "definitions": "Extracted text",
    "obligations": "Extracted text",
    "responsibilities": "Extracted text",
    "eligibility": "Extracted text",
    "payments": "Extracted text",
    "penalties": "Extracted text",
    "record_keeping": "Extracted text"
  },
  "rule_checks": [
    {
      "rule": "Act must define key terms",
      "status": "pass",
      "evidence": "Section reference or explanation",
      "confidence": 92
    }
  ]
}
```
## Key Functions

### `get_groq_client()`
- Initializes Groq client with API key
- Cached resource to avoid repeated initialization
- Returns configured Groq client instance

### `extract_pdf_text(pdf_file)`
- Accepts uploaded PDF file object
- Extracts text from all pages using pdfplumber
- Returns cleaned concatenated text
- Handles exceptions and displays error messages

### `analyze_document(text)`
- Sends document text to Groq LLM
- Constructs detailed analysis prompt with all tasks
- Parses JSON response from model
- Returns structured dictionary with results
- Implements error handling for JSON parsing failures

## Usage Guide

1. **Upload Document**: Click file uploader in sidebar, select PDF
2. **Analyze**: Click "Analyze Document" button
3. **View Results**: Browse summary, sections, and rule checks in main area
4. **Download**: Click "Download JSON Report" to save results with timestamp
5. **Clear**: Click "Clear Analysis" to reset for new document

## Limitations

- Maximum text length depends on Groq API limits (typically 4096 tokens for response)
- PDF extraction quality depends on document OCR compatibility
- Analysis accuracy varies based on document clarity and structure
- Free Groq tier has usage limits and rate restrictions

- Export to multiple formats (CSV, PDF, Word)
- Document comparison features
- API rate limit monitoring

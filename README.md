# Bajaj FinServ Invoice Data Extraction API

A FastAPI-based service that extracts line-item details from invoice images using OCR and Google's Gemini AI for intelligent data structuring.

## Features

- **Image-to-Text Extraction**: Uses Pytesseract to extract text from invoice images
- **AI-Powered Structuring**: Leverages Google Gemini 2.5 Flash to intelligently parse and structure invoice data
- **JSON Response**: Returns structured invoice data including line items, totals, and token usage metrics
- **HTTP Image Support**: Accepts image URLs and downloads them for processing

## Prerequisites

- Python 3.8+
- Tesseract OCR installed on the system
- Google API Key for Gemini access

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/swarajmali45/bajaj_finserv.git
cd bajaj_finserv
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the project root with:
```
API_KEY=your_google_gemini_api_key_here
PORT=8000
```

## Usage

### Running Locally

1. **Start the API server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

2. **Access the interactive documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

**GET `/`**
- Returns a welcome message

**GET `/add`**
- **Parameter:** `link` (string, required) - Public URL to the invoice image
- **Returns:** Structured invoice data with extracted line items and totals
- **Example:**
```bash
curl "http://localhost:8000/add?link=https://example.com/invoice.jpg"
```

### Response Format

```json
{
  "is_success": true,
  "data": {
    "pagewise_line_items": [
      {
        "page_no": "1",
        "bill_items": [
          {
            "item_name": "Product Name",
            "item_amount": 1000.00,
            "item_rate": 100.00,
            "item_quantity": 10.00
          }
        ]
      }
    ],
    "total_item_count": 1,
    "reconciled_amount": 1000.00,
    "token_usage": {
      "total_tokens": 1234,
      "input_tokens": 567,
      "output_tokens": 667
    }
  }
}
```

## Project Structure

```
bajaj_finserv/
├── main.py           # FastAPI application entry point
├── utils.py          # OCR and Gemini AI integration functions
├── requirements.txt  # Python dependencies
├── render.yaml       # Render deployment configuration
├── .env              # Environment variables (create locally)
└── README.md         # This file
```

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **opencv-python**: Image processing
- **numpy**: Numerical operations
- **requests**: HTTP client for downloading images
- **pytesseract**: OCR text extraction
- **google-generativeai**: Gemini AI integration
- **python-dotenv**: Environment variable management

## Deployment

### Deploy to Render

1. Push your code to GitHub
2. Connect your repository to Render
3. The `render.yaml` file configures the deployment:
   - Installs Tesseract during the build phase
   - Installs Python dependencies
   - Starts the Uvicorn server

4. Add `API_KEY` environment variable in Render dashboard
5. Deploy!

## Troubleshooting

**Error: "tesseract is not installed or it's not in your PATH"**
- Ensure Tesseract is installed on your system
- Add Tesseract to your system PATH
- On Windows, install via: `choco install tesseract` or download from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

**Error: "API_KEY not found in environment variables"**
- Ensure `.env` file exists with `API_KEY` set
- On Render, add `API_KEY` as an environment variable in the dashboard

**Error: "Unable to fetch image"**
- Verify the image URL is publicly accessible
- Check your internet connection
- Ensure the URL returns a valid image file

## License

This project is private. Contact the repository owner for usage rights.

## Contributing

For issues and feature requests, please create an issue or contact the repository maintainer.

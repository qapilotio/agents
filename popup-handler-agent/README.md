# Popup Handler Agent

## Overview

The Popup Handler Agent is a FastAPI-based application designed to analyze mobile screenshots and XML data to detect pop-up dialog boxes. It utilizes OpenAI's GPT-4o model to provide recommendations based on the detected pop-ups.

## Features

- **Flexible Input Methods**: Support for multiple input types for images and XML
- **Image Analysis**: Detect pop-ups from various image sources
- **XML Analysis**: Parse mobile screen hierarchies from different input formats
- **AI Integration**: Uses OpenAI's GPT-4o model to provide intelligent suggestions
- **API Endpoints**: Provides service and health check endpoints

## Installation

1. Clone the repository:

```bash
git clone https://github.com/qapilotio/agents.git
cd popup-handler-agent
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

- Create a `.env` file in the root directory.
- Add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

## Payload Format

### Input Flexibility

The `/invoke` endpoint offers multiple ways to provide input:

#### Image Input Options

You can provide the image using:

- Local file path (e.g., `/path/to/screenshot.png`)
- Image URL (e.g., `https://example.com/screenshot.jpg`)
- Base64 encoded image string

#### XML Input Options

You can provide XML using:

- Local file path containing XML
- Direct XML string
- XML URL
- In-memory XML content

### Payload Structure

| Field          | Type   | Required      | Description                                   |
| -------------- | ------ | ------------- | --------------------------------------------- |
| `testcase_dec` | string | Yes           | Description of the test case or scenario      |
| `image`        | string | Conditional\* | Image input for screen analysis               |
| `xml`          | string | Conditional\* | XML representation of mobile screen hierarchy |

\*Note: Either `image` or `xml` must be provided, but not both.

### Payload Validation

- If both `image` and `xml` are provided, a 422 Unprocessable Entity error will be returned.
- If neither `image` nor `xml` is provided, a 400 Bad Request error will be returned.

## Usage

1. Run the FastAPI application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

### POST /invoke

- **Purpose**: Analyzes mobile screen for pop-ups
- **Input**: JSON payload with test case description
- **Supported Inputs**:
  - Images: File paths, URLs, Base64 strings
  - XML: File paths, URLs, Direct strings
- **Output**: JSON response with AI-generated analysis

### GET /health

- **Purpose**: Checks the health status of the application
- **Output**: JSON with status

## Response Format

The successful response will include:

- `status`: Indicates the success of the request
- `Agent-response`: Detailed AI analysis of the pop-up
- `processed_xml`: XML processing details (if XML was provided)

## Code Structure

- **main.py**: FastAPI application setup and endpoint definitions
- **utils.py**: Utility functions for image encoding and XML parsing
- **prompts.py**: Prompts used for AI analysis
- **llm.py**: OpenAI language model initialization

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## Contact

For questions or support, please contact [Your Contact Information]

## License

[Specify your license here]

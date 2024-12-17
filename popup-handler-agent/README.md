# Popup Handler Agent

## Overview

The Popup Handler Agent is a FastAPI-based application designed to analyze mobile screenshots and XML data to detect pop-up dialog boxes, utilizing OpenAI's GPT-4o model to provide intelligent recommendations.

## Features

- Flexible input methods for images and XML
- Pop-up detection from various image sources
- Mobile screen hierarchy parsing
- AI-powered intelligent suggestions using OpenAI's GPT-4o
- Comprehensive API endpoints

## Prerequisites

- Python
- OpenAI API Key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/qapilotio/agents.git
   cd popup-handler-agent
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Create a `.env` file
   - Add OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

1. Start the application:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. Access API documentation at `http://localhost:8000/docs`

## API Endpoints

### POST /invoke

- Analyzes mobile screen for pop-ups
- Supports various image and XML inputs
- Returns AI-generated analysis

#### Payload Structure

The `/invoke` endpoint accepts a JSON payload with:

| Field          | Type   | Required      | Description                 | Input Options                       |
| -------------- | ------ | ------------- | --------------------------- | ----------------------------------- |
| `testcase_dec` | string | Yes           | Test case description       | Free-text description               |
| `image`        | string | Conditional\* | Screen analysis image       | - Local file path<br>- URL to image |
| `xml`          | string | Conditional\* | Mobile screen hierarchy XML | - Local file path<br>- URL to XML   |

\*Note: Either `image` or `xml` must be provided, but not both.

### GET /health

- Checks application status

## Response Format

Successful response includes:

- `status`: Request success indicator
- `Agent-response`:
  - `popup_detection`: Pop-up presence ("Yes"/"No")
  - `suggested_action`: Recommended action
  - `element_metadata`: Detailed element information (XML input)

## Project Structure

- `main.py`: FastAPI application setup
- `utils.py`: Utility functions
- `prompts.py`: AI analysis prompts
- `llm.py`: OpenAI model initialization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Submit a pull request

## Contact

For questions or support, please contact [Your Contact Information]

## License

[Specify your license here]

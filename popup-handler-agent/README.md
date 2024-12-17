# Popup Handler Agent

## Overview

The Popup Handler Agent is a FastAPI-based application designed to analyze mobile screenshots and XML data to detect pop-up dialog boxes. It utilizes OpenAI's GPT-4o model to provide recommendations based on the detected pop-ups.

## Features

- **Image Analysis**: Encodes images and analyzes them to detect pop-ups.
- **XML Analysis**: Parses XML data to identify pop-up elements and extract relevant details.
- **AI Integration**: Uses OpenAI's GPT-4o model to provide suggestions based on the detected pop-ups.
- **API Endpoints**: Provides endpoints for running the service.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd popup-handler-agent
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the pop-up-handler-agent directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

1. Run the FastAPI application:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. Access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

- **POST /run_service**: Accepts an image or XML input and returns the analysis results.
- **GET /health_check**: Returns the health status of the application.

## Code Structure

- **main.py**: Contains the FastAPI application setup and endpoint definitions.
- **utils.py**: Provides utility functions for image encoding and XML parsing.
- **prompts.py**: Contains the prompts used for AI analysis.
- **llm.py**: Initializes the OpenAI language model.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or support, please contact [your-email@example.com].

# CharlieB Chat Application

This application provides a chat interface powered by a local Large Language Model (LLM) for querying documents.

## Overview

The application consists of a FastAPI backend and a React frontend. The backend uses LM Studio to run an LLM for generating answers and embeddings, while the frontend provides a user-friendly chat widget.

## Features

* **Local LLM:** Uses LM Studio to run LLMs locally, ensuring data privacy.
* **Document Querying:** Allows users to ask questions about documents stored in a specified directory.
* **Chat Interface:** Provides a simple and intuitive chat interface.
* **Health Check:** Includes a health check endpoint to verify backend availability.
* **CORS Support:** Configured to allow cross-origin requests from the frontend.
* **Error Handling:** Implements robust error handling and logging.
* **Loading State:** Provides a loading indicator during backend processing.
* **Accessibility:** Includes ARIA attributes for improved accessibility.

## Technologies Used

* **Backend:**
    * FastAPI
    * Python
    * LM Studio
    * LlamaIndex
    * Ollama
    * Pydantic
    * Requests
* **Frontend:**
    * React
    * TypeScript
    * Tailwind CSS

## Setup and Installation

### Prerequisites

* Python 3.12 or higher
* Node.js and npm
* LM Studio (with `text-embedding-nomic-embed-text-v1.5@q8_0` and `meta-llama-3-8b-instruct` models loaded)
* Ollama

### Backend Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd app/backend
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    venv\Scripts\activate # On Windows
    source venv/bin/activate # On macOS and Linux
    ```

3.  **Install dependencies:**

    ```bash
    pip install fastapi uvicorn llama-index requests pydantic ollama
    ```

4.  **Run the backend:**

    ```bash
    uvicorn main:app --reload
    ```

    The backend will be available at `http://127.0.0.1:8000`.

### Frontend Installation

1.  **Navigate to the frontend directory:**

    ```bash
    cd ../frontend
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    ```

3.  **Run the frontend:**

    ```bash
    npm run dev
    ```

    The frontend will be available at `http://127.0.0.1:5173`.

### Configuration

* **Backend:**
    * The document directory is configured in `llama_index_loader.py`. Modify the `directory_path` variable to point to your documents.
    * The embedding and language models are configured in `llama_index_loader.py` and `lmstudio_wrapper.py`. Ensure that the models are loaded in LM Studio.
    * The LLM is configured to use Ollama, so ensure that Ollama is running, and can communicate with LM Studio.
* **Frontend:**
    * The backend URL is configured in `chatwidget.tsx`. Modify the `fetch` URLs if your backend is running on a different port.

## Usage

1.  Start LM Studio, Ollama, the backend, and the frontend.
2.  Open the frontend in your browser (`http://127.0.0.1:5173`).
3.  Click the chat icon to open the chat widget.
4.  Enter your question and click "Send".
5.  The bot will respond with an answer based on the documents in the specified directory.

## File Structure

app/
├── backend/
│   ├── api/
│   │   └── routes.py
│   ├── llm/
│   │   └── lmstudio_wrapper.py
│   ├── utils/
│   │   └── llama_index_loader.py
│   ├── main.py
│   └── ...
├── frontend/
│   ├── src/
│   │   └── ChatWidget.tsx
│   ├── public/
│   └── ...
├── data/ # Place your documents here
└── README.md


## Improvements

* Implement a typing indicator.
* Add more robust error handling.
* Implement more detailed logging.
* Add better parsing of the LLM responses.
* Add summarization of the LLM responses.
* Add more robust input validation.
* Add unit tests.
* Implement CI/CD.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

## License

[MIT](LICENSE)
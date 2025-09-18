CogniChat 📚🤖
CogniChat is a powerful, locally-hosted web application that allows you to have an interactive conversation with your PDF documents. Built with a modern tech stack, this project uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware answers based only on the content of your uploaded file.

The entire application runs on your local machine, ensuring your data remains completely private and secure. No API keys are required.

✨ Features
Interactive Chat Interface: Ask questions in natural language and get answers directly from your PDF.

100% Local & Private: Uses the locally-running Ollama to run powerful LLMs like Llama 3 on your own machine. Your documents and conversations never leave your computer.

Document-Grounded Answers: The AI is instructed to answer questions based only on the provided document, preventing hallucinations or fabricated answers.

Modern Tech Stack: Built with a React frontend, a FastAPI backend, and LangChain for the core AI logic.

Simple & Clean UI: An intuitive interface for uploading files and chatting, making it easy for anyone to use.

⚙️ Tech Stack & Architecture
This project is composed of two main parts: a frontend web application and a backend server.

Frontend:

React: For building the dynamic user interface.

Axios: For making asynchronous HTTP requests to the backend.

CSS: For custom styling and a responsive layout.

Backend:

FastAPI: A modern, high-performance Python web framework for building the API.

LangChain: The core framework for orchestrating the RAG (Retrieval-Augmented Generation) pipeline.

Ollama: For serving the local Large Language Model (e.g., Llama 3) that powers the chat.

Sentence-Transformers: For generating the text embeddings (vector representations of text).

ChromaDB: An in-memory vector database to store and retrieve document embeddings efficiently.

PyPDFLoader: For loading and parsing text content from PDF documents.

Project Flow
The user uploads a PDF file via the React frontend.

The file is sent to the FastAPI backend.

LangChain uses PyPDFLoader to load the document and RecursiveCharacterTextSplitter to break it into smaller, manageable chunks.

Each chunk is converted into a numerical vector (an embedding) using HuggingFaceEmbeddings.

These embeddings are stored in-memory in a Chroma vector store.

When the user asks a question, the backend performs a similarity search in the vector store to find the most relevant document chunks.

These relevant chunks are passed to the Ollama LLM as context, along with the user's original question.

The LLM generates an answer based on the provided context, which is then sent back to the user in the chat interface.

🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.

Prerequisites
Make sure you have the following installed on your system:

Node.js and npm: Download Node.js (npm is included)

Python 3.8+: Download Python

Ollama: Download Ollama

1. Set up the Local LLM with Ollama
After installing Ollama, you need to pull a model from the library. We recommend Llama 3, which is powerful and efficient for this task.

Open your terminal and run:

ollama pull llama3

Ensure the Ollama application is running in the background before proceeding to the next step.

2. Backend Setup
Navigate to the backend directory and set up the Python environment.

# Go to the backend folder
cd backend

# Create and activate a virtual environment
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate

# Install the required Python packages
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload

The backend server will now be running at http://localhost:8000. Keep this terminal window open.

3. Frontend Setup
Open a new terminal window and navigate to the frontend directory.

# Go to the frontend folder
cd frontend

# Install the required npm packages
npm install

# Start the React development server
npm start

Your web browser should automatically open to http://localhost:3000, where you can use the application.

使い方 (How to Use)
Open the Application: Navigate to http://localhost:3000 in your browser.

Upload PDF: Click "Choose File" and select a PDF document from your computer.

Process: Click the "Upload" button. The backend will process the file, which may take a moment depending on its size. The status message will update you on the progress.

Ask Questions: Once the status says "Ready...", type your questions into the chat box and get answers sourced directly from your document!

🌳 File Structure
CogniChat/
├── backend/
│   ├── venv/
│   ├── main.py             # FastAPI application logic
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── node_modules/
│   ├── public/
│   └── src/
│       ├── App.css         # Styles for the application
│       ├── App.js          # Main React component
│       └── index.js        # Entry point for React
│
└── README.md               # This file

🛠️ Future Improvements
[ ] Support for more document types (e.g., .txt, .docx, .md).

[ ] Display the source chunks that were used to generate each answer for verification.

[ ] Persist vector stores to disk to avoid re-processing the same file on restart.

[ ] Add loading spinners and more detailed status messages for a better UX.

[ ] Dockerize the entire application for a one-command setup.

📄 License
This project is licensed under the MIT License.

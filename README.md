# CogniChat 📚🤖

An interactive, locally-hosted web app that lets you have intelligent conversations with PDF documents. Built with modern tools—React, FastAPI, LangChain—and powered by locally running language models (e.g. Llama 3 via Ollama). Your documents stay private, since nothing is sent to remote APIs.

---

## 🚀 Features

* **Interactive Chat Interface** — Ask natural-language questions to your PDF and get answers grounded in its content.
* **Fully Local & Private** — Uses Ollama / Llama 3 / Gemma3:1b running on your computer; no need for external API keys.
* **Document-Grounded Answers** — Answers are based *only* on the uploaded document, avoiding hallucinations.
* **Modern Tech Stack** — React frontend, FastAPI backend, LangChain for RAG logic.
* **Clean UI / UX** — Intuitive layout; simple upload + question workflow.

---

## 🧰 Tech Stack & Architecture

| Component                 | Purpose                                                   |
| ------------------------- | --------------------------------------------------------- |
| **React**                 | Frontend UI, dynamic chat and file upload.                |
| **Axios**                 | Handling HTTP requests from front → back.                 |
| **FastAPI**               | Serving backend endpoints; orchestrates AI logic.         |
| **LangChain**             | Implements RAG (Retrieval-Augmented Generation) pipeline. |
| **Ollama**                | Local LLM provider (e.g. Llama 3).                        |
| **Sentence-Transformers** | Creates embeddings for document chunks.                   |
| **ChromaDB**              | Vector database for storing/retrieving embeddings.        |
| **PyPDFLoader**           | Parses PDF content into text.                             |

---

## ⚙️ How it Works (Workflow)

1. Upload a PDF via the React frontend.
2. Frontend sends the file to the backend.
3. Backend uses `PyPDFLoader` to extract text and `RecursiveCharacterTextSplitter` to split into smaller chunks.
4. Chunks are embedded (via `HuggingFaceEmbeddings` / Sentence-Transformers) and stored in ChromaDB.
5. When you ask a question, a similarity search retrieves the most relevant text chunks.
6. These chunks + your question are fed to the local LLM (via Ollama).
7. The LLM returns an answer, which is displayed to you.

---

## 🛠️ Getting Started (Setup Instructions)

### Prerequisites

* Node.js + npm
* Python 3.8+
* Ollama installed and set up
* (Optional but recommended) Virtual environment for Python

### Setup Steps

```bash
# Clone the repo
git clone https://github.com/Tusharsinghchauh/CogniChat.git
cd CogniChat

# 1. Pull a model with Ollama
ollama pull llama3
# Ensure Ollama is running

# 2. Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate        # On Unix/macOS
# or for Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload        # starts backend at http://localhost:8000

# 3. Frontend setup
cd ../frontend
npm install
npm start                        # opens http://localhost:3000
```

---

## 🔍 Usage

1. Open the browser at `http://localhost:3000`.
2. Upload your PDF file using the upload interface.
3. Wait until it's processed.
4. Ask questions using the chat box. Answers will be based on the document.

---

## 📂 Project Structure

```
CogniChat/
├── backend/
│   ├── main.py               # FastAPI app & endpoints
│   ├── requirements.txt      # Python dependencies
│   └── …                     # Other modules and utils
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── index.js          # React entry point
│   │   └── …                 # Other components/assets
│   └── package.json
├── .gitignore
└── README.md
```

---

## 🔮 Future Improvements

* [ ] Support more document formats (e.g. `.txt`, `.docx`, `.md`)
* [ ] Persist vector stores so you don’t need to re-process the same file each session
* [ ] Show which document chunks the answer came from (for more transparency)
* [ ] Polish UI: loading spinners, status messages
* [ ] Dockerize for easy one-command setup

---

## 📄 License

This project is licensed under the **MIT License**.


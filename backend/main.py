# 1. Import necessary libraries
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
import tempfile
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


# --- EXPLANATION OF IMPORTS ---
# FastAPI: The main framework for building our API.
# UploadFile, File, Form: Used to handle file uploads from the frontend.
# CORSMiddleware: Allows our React frontend (running on a different port) to communicate with our backend.
# PyPDFLoader: A LangChain tool to load and read text content from PDF files.
# RecursiveCharacterTextSplitter: A LangChain tool to split a long document into smaller chunks.
# HuggingFaceEmbeddings: Converts text chunks into numerical vectors (embeddings) using free models from Hugging Face.
# Chroma: A vector database to store the embeddings and search for them efficiently.
# ChatOllama: The LangChain integration for the Ollama model we are running locally.
# ChatPromptTemplate: Helps create a structured prompt for the LLM.
# RunnablePassthrough: A LangChain tool to pass input through the chain unchanged.
# StrOutputParser: A LangChain tool to parse the LLM's output into a simple string.


# 2. Initialize the FastAPI app
app = FastAPI()

# 3. Setup CORS Middleware
# This is crucial for allowing the frontend to make requests to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The origin of our React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# 4. Global variable to hold the RAG chain
# We will create the chain when a file is uploaded and store it here.
rag_chain = None

# --- EXPLANATION OF SETUP ---
# app = FastAPI(): Creates an instance of the FastAPI application.
# app.add_middleware(...): Configures CORS. Without this, your browser would block the React app's request to this server for security reasons.
# rag_chain = None: We declare a global variable to hold our main LangChain logic. It's `None` initially because no file has been uploaded yet.
# 5. Create the file upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global rag_chain

    # --- EXPLANATION OF ENDPOINT ---
    # @app.post("/upload"): Defines an HTTP POST endpoint at the URL `/upload`.
    # async def ...: Defines an asynchronous function, which is efficient for I/O operations like saving a file.
    # file: UploadFile: FastAPI automatically handles the incoming file and provides it in this variable.

    # Use a temporary file to securely handle the upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # --- EXPLANATION OF FILE HANDLING ---
        # We save the file to disk because PyPDFLoader needs a file path to read from.
        # Using `tempfile` is safer than creating a filename manually.

        # 2. Load the PDF
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()
        
        # --- EXPLANATION OF LOADER ---
        # PyPDFLoader(temp_file_path): Creates an instance of the PDF loader.
        # loader.load(): Reads the PDF and loads its content into a list of "Document" objects.

        # 3. Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # --- EXPLANATION OF SPLITTER ---
        # Why split? LLMs have a limited context window (they can't "read" a whole book at once).
        # We split the doc into smaller, overlapping chunks to feed into the model.
        # chunk_size=1000: Each chunk will be around 1000 characters.
        # chunk_overlap=200: Each chunk will share 200 characters with the previous one to maintain context.

        # 4. Create embeddings and store in a vector database (Chroma)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

        # --- EXPLANATION OF EMBEDDINGS & VECTORSTORE ---
        # Embeddings are numerical representations of text. "King" and "Queen" would have similar numbers.
        # HuggingFaceEmbeddings(...): We're using a popular, free model to create these embeddings.
        # Chroma.from_documents(...): This one-line command creates the embeddings for all text splits and stores them in the Chroma vector database in memory.

        # 5. Define the RAG chain
        retriever = vectorstore.as_retriever()
        
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        llm = ChatOllama(model="gemma3:1b")

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # --- EXPLANATION OF THE RAG CHAIN ---
        # (Explanation remains the same)

    except Exception as e:
        # If there's an error during processing, return an error message
        raise HTTPException(status_code=400, detail=f"Failed to process PDF: {e}")
    finally:
        # 6. Clean up the temporary file
        os.remove(temp_file_path)

    return {"status": "File processed successfully"}

# 6. Create the chat endpoint
@app.post("/chat")
async def chat_with_doc(question: str = Form(...)):
    if rag_chain is None:
        raise HTTPException(status_code=400, detail="Please upload a document first.")
    
    # --- EXPLANATION OF CHAT ENDPOINT ---
    # This endpoint receives a "question" from the frontend.
    # It first checks if the rag_chain has been created (i.e., if a file has been uploaded).

    # 7. Invoke the chain to get an answer
    response = rag_chain.invoke(question)
    
    # --- EXPLANATION OF INVOKE ---
    # .invoke(question): This is how you run the chain. The question is passed in, and it goes through the entire flow we defined earlier.
    
    return {"answer": response}    
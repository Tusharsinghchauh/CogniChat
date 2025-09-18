import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// --- EXPLANATION OF IMPORTS ---
// React, useState: The core React library and the `useState` hook for managing component state.
// axios: The library for making API calls to our backend.
// ./App.css: Our stylesheet.

function App() {
  // --- STATE MANAGEMENT WITH useState ---
  // file: Stores the PDF file selected by the user. Initially null.
  const [file, setFile] = useState(null);
  // question: Stores the question typed by the user in the input box. Initially an empty string.
  const [question, setQuestion] = useState('');
  // chatHistory: An array to store the conversation. Each item is an object { type, text }.
  const [chatHistory, setChatHistory] = useState([]);
  // status: A message to show the user what's happening (e.g., "Uploading...", "Ready").
  const [status, setStatus] = useState('Select a PDF to begin.');

  // --- EVENT HANDLERS ---

  // Called when the user selects a file.
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setStatus('File selected. Click Upload.');
  };

  // Called when the user clicks the "Upload" button.
  const handleUpload = async () => {
    if (!file) {
      setStatus('Please select a file first.');
      return;
    }
    // FormData is a special object for sending files and text in an HTTP request.
    const formData = new FormData();
    formData.append('file', file);

    setStatus('Uploading and processing...');
    try {
      // Make the POST request to the /upload endpoint on our FastAPI backend.
      await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatus(`Ready to answer questions about ${file.name}.`);
    } catch (error) {
      console.error('Error uploading file:', error);
      setStatus('Error uploading file. Please try again.');
    }
  };

  // Called when the user types in the question input box.
  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  // Called when the user submits a question (clicks Ask or presses Enter).
  const handleAsk = async (event) => {
    event.preventDefault(); // Prevents the webpage from reloading on form submission.
    if (!question) {
      return;
    }
    // Add user's question to chat history to display it on the screen.
    setChatHistory(prev => [...prev, { type: 'user', text: question }]);
    setStatus('Thinking...');

    try {
      // FormData is also used here to send the text question.
      const formData = new FormData();
      formData.append('question', question);

      // Make the POST request to the /chat endpoint.
      const response = await axios.post('http://localhost:8000/chat', formData);
      
      // Add the AI's answer to the chat history.
      setChatHistory(prev => [...prev, { type: 'ai', text: response.data.answer }]);
      setQuestion(''); // Clear the input box
      setStatus('Ready for your next question.');

    } catch (error) {
      console.error('Error asking question:', error);
      setStatus('Error getting an answer. Please try again.');
    }
  };

  // --- JSX: THE UI STRUCTURE ---
  return (
    <div className="App">
      <header className="App-header">
        <h1>Chat With Your PDF 📚</h1>
        <p className="status">{status}</p>
      </header>
      
      <div className="upload-section">
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
      </div>

      <div className="chat-section">
        <div className="chat-history">
          {chatHistory.map((entry, index) => (
            <div key={index} className={`message ${entry.type}`}>
              <p>{entry.text}</p>
            </div>
          ))}
        </div>
        <form onSubmit={handleAsk} className="chat-input">
          <input
            type="text"
            value={question}
            onChange={handleQuestionChange}
            placeholder="Ask a question about the document..."
          />
          <button type="submit">Ask</button>
        </form>
      </div>
    </div>
  );
}

export default App;
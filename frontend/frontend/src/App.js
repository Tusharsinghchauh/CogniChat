import React, { useState } from 'react';
import axios from 'axios';
import './App.css';


function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [status, setStatus] = useState('Select a PDF to begin.');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setStatus('File selected. Click Upload.');
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus('Please select a file first.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    setStatus('Uploading and processing...');
    try {
      await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatus(`Ready to answer questions about ${file.name}.`);
    } catch (error) {
      console.error('Error uploading file:', error);
      setStatus('Error uploading file. Please try again.');
    }
  };

  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleAsk = async (event) => {
    event.preventDefault(); 
    if (!question) {
      return;
    }
    setChatHistory(prev => [...prev, { type: 'user', text: question }]);
    setStatus('Thinking...');

    try {
      const formData = new FormData();
      formData.append('question', question);

      const response = await axios.post('http://localhost:8000/chat', formData);
      
      setChatHistory(prev => [...prev, { type: 'ai', text: response.data.answer }]);
      setQuestion(''); 
      setStatus('Ready for your next question.');

    } catch (error) {
      console.error('Error asking question:', error);
      setStatus('Error getting an answer. Please try again.');
    }
  };

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

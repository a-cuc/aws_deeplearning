import React, { useState } from 'react';

export default function SimpleUpload({ setPrediction, setInputData }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');

  // 1. Intercept file selection and run initial validation
  const handleFileChange = (e) => {
    setError('');
    setStatus('');
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) return;

    // Strict validation: Check extension and mime type
    const isJsonExt = selectedFile.name.endsWith('.json');
    const isJsonMime = selectedFile.type === 'application/json';

    if (!isJsonExt && !isJsonMime) {
      setError('Strict Error: Invalid file type. Only .json files are permitted.');
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  // 2. Read the file contents and strictly check the JSON syntax
  const handleUpload = () => {
    if (!file) return setError('Please select a file first.');
    setError('');
    setStatus('Processing...');

    const reader = new FileReader();

    // Triggered once the file is fully read into memory
    reader.onload = async (event) => {
      const fileContent = event.target?.result;

      try {
        // Strict Error Check: This throws a syntax error if JSON layout is malformed
        const parsedJson = JSON.parse(fileContent);
        setInputData(parsedJson); // Store the parsed JSON for later use
        
        // OPTIONAL: Add content rules here (e.g., if (!parsedJson.id) throw new Error('Missing ID'))

        setStatus('Uploading...');
        const response = await fetch('http://localhost:3000/predict', {
          method: 'POST',
          body: fileContent,
        });

        if (!response.ok) {
          throw new Error(`Server rejected file with status: ${response.status}`);
        }

        const predictionResult = await response.json();

        setPrediction(predictionResult.predicted_result);
        setStatus('File successfully validated and uploaded!');
        setFile(null);
      } catch (err) {
        // Catch syntax errors from JSON.parse or server response rejections
        setStatus('');
        setError(`Error: ${err.message}`);
      }
    };

    reader.onerror = () => {
      setError('Error: Could not read the file from disk.');
    };

    // Read the binary file object as raw text
    reader.readAsText(file);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      {/* 'accept' parameter hints to the OS to only show JSON files */}
      <input type="file" accept=".json,application/json" onChange={handleFileChange} />
      
      <div style={{ margin: '15px 0' }}>
        <button onClick={handleUpload} disabled={!file}>Upload JSON</button>
      </div>

      {status && <p style={{ color: 'blue', fontWeight: 'bold' }}>{status}</p>}
      {error && <p style={{ color: 'red', fontWeight: 'bold', whiteSpace: 'pre-wrap' }}>{error}</p>}
    </div>
  );
}
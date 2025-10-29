import React, { useState } from "react";
import { uploadFile } from "./api";

import "./App.css";
function App() {
  const [file, setFile] = useState(null);
  const [targetLangs, setTargetLangs] = useState("en,hi");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return alert("Choose file");
    setLoading(true);
    try {
      const data = await uploadFile(file, 'pt', targetLangs);
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Error: " + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h2>Law Document Translator (PT → EN / HI / Konkani)</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={(e)=>setFile(e.target.files[0])} />
        <div className="target-languages">
          <label>Target languages (comma separated): </label>
          <input value={targetLangs} onChange={(e)=>setTargetLangs(e.target.value)} />
        </div>
        <button type="submit" className="submit-button" disabled={loading}>Translate</button>
      </form>

      {loading && <p className="loading-message">Processing... this can take a while for large PDFs.</p>}

      {result && (
        <div className="result-container">
          <h3>Extracted Text</h3>
          <pre className="result-text">{result.extracted_text}</pre>

          <h3>Translations</h3>
          {Object.entries(result.translations).map(([lang, text]) => (
            <div key={lang} className="translation">
              <h4>{lang}</h4>
              <pre className="result-text">{text}</pre>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App;
import React, { useState } from 'react';
import axios from 'axios';
import styles from '@/styles/OllamaInterface.module.css';

const OllamaInterface: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedModel, setSelectedModel] = useState('llama2');
  const [useRAG, setUseRAG] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResponse('');

    try {
      let result;
      if (useRAG) {
        result = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/rag`, {
          query: prompt,
          model: selectedModel
        });
      } else {
        result = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/generate`, {
          prompt,
          model: selectedModel
        });
      }
      setResponse(result.data.generated_text);
    } catch (err) {
      setError('Failed to generate response. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Ollama Generate API</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className={styles.select}
        >
          <option value="llama2">Llama 2</option>
          <option value="llama3.2">Llama 3.2</option>
        </select>
        <label>
          <input
            type="checkbox"
            checked={useRAG}
            onChange={(e) => setUseRAG(e.target.checked)}
          />
          Use RAG
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt here..."
          className={styles.textarea}
          rows={4}
        />
        <button type="submit" className={styles.button} disabled={loading}>
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </form>
      {error && <p className={styles.error}>{error}</p>}
      {response && (
        <div className={styles.response}>
          <h3>Generated Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default OllamaInterface;

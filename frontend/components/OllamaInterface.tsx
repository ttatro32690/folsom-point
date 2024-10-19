import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import styles from '@/styles/OllamaInterface.module.css';

const OllamaInterface: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedModel, setSelectedModel] = useState('llama2');
  const [useRAG, setUseRAG] = useState(false);
  const responseRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (responseRef.current) {
      responseRef.current.scrollTop = responseRef.current.scrollHeight;
    }
  }, [response]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResponse('');

    try {
      const endpoint = useRAG ? '/api/rag/stream' : '/api/generate/stream';
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt,
          model: selectedModel,
          query: prompt, // for RAG endpoint
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No reader available');
      }

      setResponse('');
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = new TextDecoder().decode(value);
        setResponse((prev) => prev + text);
      }
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
        <div className={styles.controls}>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className={styles.select}
          >
            <option value="llama2">Llama 2</option>
            <option value="llama3.2">Llama 3.2</option>
          </select>
          <label className={styles.ragLabel}>
            <input
              type="checkbox"
              checked={useRAG}
              onChange={(e) => setUseRAG(e.target.checked)}
            />
            Use RAG
          </label>
        </div>
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
      <div className={styles.responseContainer}>
        <h3>Generated Response:</h3>
        <div className={styles.response} ref={responseRef}>
          {response}
        </div>
      </div>
    </div>
  );
};

export default OllamaInterface;

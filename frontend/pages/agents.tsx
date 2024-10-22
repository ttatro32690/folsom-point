import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Typography, TextField, Button, Box, CircularProgress } from '@mui/material';

const AgentsPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResponse('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/agent/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          model: 'llama2', // You can make this selectable if you want to support multiple models
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No reader available');
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = new TextDecoder().decode(value);
        setResponse((prevResponse) => prevResponse + text);
      }
    } catch (err) {
      setError('Failed to get response from agent. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        AI Agent Interface
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          label="Enter your query"
          variant="outlined"
          value={query}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setQuery(e.target.value)}
          margin="normal"
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
          sx={{ mt: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Submit'}
        </Button>
      </form>
      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}
      {response && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6">Agent Response:</Typography>
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
            {response}
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default AgentsPage;

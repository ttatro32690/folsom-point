import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import styles from '@/styles/ContextManager.module.css';

interface Context {
  _id: string;
  _source: {
    title: string;
    content: string;
  };
}

const ContextManager: React.FC = () => {
  const [contexts, setContexts] = useState<Context[]>([]);
  const [newContext, setNewContext] = useState({ title: '', content: '' });
  const [editingContext, setEditingContext] = useState<Context | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchContexts = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/context`);
      setContexts(response.data.contexts);
    } catch (error) {
      console.error('Error fetching contexts:', error);
      setError('Failed to fetch contexts. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchContexts();
  }, [fetchContexts]);

  const addContext = async () => {
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/context`, newContext);
      setNewContext({ title: '', content: '' });
      fetchContexts();
    } catch (error) {
      console.error('Error adding context:', error);
      setError('Failed to add context. Please try again.');
    }
  };

  const deleteContext = async (id: string) => {
    try {
      await axios.delete(`${process.env.NEXT_PUBLIC_API_URL}/api/context/${id}`);
      fetchContexts();
    } catch (error) {
      console.error('Error deleting context:', error);
      setError('Failed to delete context. Please try again.');
    }
  };

  const updateContext = async () => {
    if (!editingContext) return;
    try {
      await axios.put(`${process.env.NEXT_PUBLIC_API_URL}/api/context/${editingContext._id}`, editingContext._source);
      setEditingContext(null);
      fetchContexts();
    } catch (error) {
      console.error('Error updating context:', error);
      setError('Failed to update context. Please try again.');
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Context Manager</h2>
      {error && <p className={styles.error}>{error}</p>}
      <div className={styles.addContext}>
        <input
          type="text"
          placeholder="Title"
          value={newContext.title}
          onChange={(e) => setNewContext({ ...newContext, title: e.target.value })}
        />
        <textarea
          placeholder="Content"
          value={newContext.content}
          onChange={(e) => setNewContext({ ...newContext, content: e.target.value })}
        />
        <button onClick={addContext}>Add Context</button>
      </div>
      {isLoading ? (
        <p>Loading contexts...</p>
      ) : (
        <div className={styles.contextList}>
          {contexts.map((context) => (
            <div key={context._id} className={styles.contextItem}>
              {editingContext && editingContext._id === context._id ? (
                <>
                  <input
                    type="text"
                    value={editingContext._source.title}
                    onChange={(e) => setEditingContext({ ...editingContext, _source: { ...editingContext._source, title: e.target.value } })}
                  />
                  <textarea
                    value={editingContext._source.content}
                    onChange={(e) => setEditingContext({ ...editingContext, _source: { ...editingContext._source, content: e.target.value } })}
                  />
                  <button onClick={updateContext}>Save</button>
                  <button onClick={() => setEditingContext(null)}>Cancel</button>
                </>
              ) : (
                <>
                  <h3>{context._source.title}</h3>
                  <p>{context._source.content}</p>
                  <button onClick={() => setEditingContext(context)}>Edit</button>
                  <button onClick={() => deleteContext(context._id)}>Delete</button>
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ContextManager;

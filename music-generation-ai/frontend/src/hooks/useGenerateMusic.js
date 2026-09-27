import { useState, useEffect } from 'react';

const API_BASE = 'http://127.0.0.1:8000';

export function useGenerateMusic() {
  const [seeds, setSeeds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resultUrl, setResultUrl] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/seeds`)
      .then((res) => res.json())
      .then((data) => setSeeds(data.seeds))
      .catch(() => setError('Could not reach the backend.'));
  }, []);

  const generate = async ({ seedName, numNotes, temperature }) => {
    setLoading(true);
    setError(null);
    setResultUrl(null);

    try {
      const res = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          seed_name: seedName,
          num_notes: numNotes,
          temperature: temperature,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Generation failed.');
      }

      setResultUrl(`${API_BASE}${data.download_url}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { seeds, loading, error, resultUrl, generate };
}
import { TextField, Button, Box } from '@mui/material';
import { useState } from 'react';

interface QuizGeneratorProps {
  onProblemsGenerated: (problems: string[]) => void;
}

function QuizGenerator({ onProblemsGenerated }: QuizGeneratorProps) {
  const [query, setQuery] = useState('');

  const handleGenerate = async () => {
    try {
      const response = await fetch('/api/problems/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_query: query }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      onProblemsGenerated(data.Problems);
      setQuery('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Box sx={{ mb: 4, display: 'flex', gap: 2 }}>
      <TextField
        fullWidth
        label="Quiz topic?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button variant="contained" onClick={handleGenerate}>
        Generate
      </Button>
    </Box>
  );
}

export default QuizGenerator;
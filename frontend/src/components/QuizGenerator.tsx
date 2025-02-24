import { TextField, Button, Box, CircularProgress } from '@mui/material';
import { useState } from 'react';

interface QuizGeneratorProps {
  onProblemsGenerated: (problems: string[]) => void;
}

function QuizGenerator({ onProblemsGenerated }: QuizGeneratorProps) {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async () => {
    try {
      setIsLoading(true);
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
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box sx={{ mb: 4, display: 'flex', gap: 2 }}>
      <TextField
        fullWidth
        label="Quiz topic?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={isLoading}
      />
      <Button 
        variant="contained" 
        onClick={handleGenerate}
        disabled={isLoading}
        startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : null}
      >
        {isLoading ? 'Generating...' : 'Generate'}
      </Button>
    </Box>
  );
}

export default QuizGenerator;
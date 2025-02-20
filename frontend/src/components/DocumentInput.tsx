import { TextField, Button, Box } from '@mui/material';
import { useState } from 'react';

function DocumentInput() {
  const [url, setUrl] = useState('');

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:8000/crawl/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      setUrl('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Box sx={{ mb: 4, display: 'flex', gap: 2 }}>
      <TextField
        fullWidth
        label="Source Documentation"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <Button variant="contained" onClick={handleSubmit}>
        Pull Source Docs
      </Button>
    </Box>
  );
}

export default DocumentInput;
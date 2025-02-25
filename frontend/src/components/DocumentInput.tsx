import { TextField, Button, Box, Alert } from '@mui/material';
import { useState } from 'react';

function DocumentInput() {
  const [url, setUrl] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/crawl/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      setShowSuccess(true);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
    if (showSuccess) {
      setShowSuccess(false);
    }
  };

  return (
    <Box sx={{ mb: 4 }}>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          fullWidth
          label="Source Documentation"
          value={url}
          onChange={handleUrlChange}
        />
        <Button variant="contained" onClick={handleSubmit}>
          Pull Source Docs
        </Button>
      </Box>
      {showSuccess && (
        <Alert severity="success" sx={{ mt: 1 }}>
          Source documentation imported successfully!
        </Alert>
      )}
    </Box>
  );
}
export default DocumentInput;

import { TextField, Button, Box, Alert, Modal, Typography } from '@mui/material';
import { useState } from 'react';

function DocumentInput() {
  const [url, setUrl] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [topicName, setTopicName] = useState('');

  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/ingest/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          url,
          topic: topicName 
        }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      setShowSuccess(true);
      setTopicName('');
      setUrl('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleModalConfirm = () => {
    setIsModalOpen(false);
    handleSubmit();
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setTopicName('');
    setUrl('');
  };

  const modalStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    boxShadow: 24,
    p: 4,
    borderRadius: 2,
  };

  const isFormValid = url.trim() && topicName.trim();

  return (
    <Box sx={{ mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'center' }}>
        <Button 
          variant="contained" 
          onClick={() => setIsModalOpen(true)}
          sx={{ width: '300px' }}
        >
          Add New Docs
        </Button>
      </Box>

      {showSuccess && (
        <Alert severity="success" sx={{ mt: 1 }}>
          Source documentation imported successfully!
        </Alert>
      )}

      <Modal
        open={isModalOpen}
        onClose={handleModalClose}
        aria-labelledby="topic-modal-title"
      >
        <Box sx={modalStyle}>
          <Typography id="topic-modal-title" variant="h6" component="h2" sx={{ mb: 3 }}>
            Add New Documentation
          </Typography>
          
          <TextField
            fullWidth
            label="Source Documentation URL"
            value={url}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUrl(e.target.value)}
            sx={{ mb: 2 }}
          />
          
          <TextField
            fullWidth
            label="Topic Name"
            value={topicName}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTopicName(e.target.value)}
            sx={{ mb: 3 }}
          />
          
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button onClick={handleModalClose}>Cancel</Button>
            <Button 
              variant="contained" 
              onClick={handleModalConfirm}
              disabled={!isFormValid}
            >
              Confirm
            </Button>
          </Box>
        </Box>
      </Modal>
    </Box>
  );
}

export default DocumentInput;

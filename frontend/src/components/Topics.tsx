import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent, CircularProgress, Box } from '@mui/material';
import { useEffect, useState } from 'react';

interface TopicsProps {
  onTopicChange: (topic: string) => void;
}

interface TopicsResponse {
  sources: string[];
}

export default function Topics({ onTopicChange }: TopicsProps) {
  const [topics, setTopics] = useState<string[]>([]);
  const [selectedTopic, setSelectedTopic] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('/api/topics');
        if (!response.ok) {
          throw new Error('Failed to fetch topics');
        }
        const data: TopicsResponse = await response.json();
        
        if (!data.sources || !Array.isArray(data.sources)) {
          throw new Error('Invalid topics data received');
        }
        
        setTopics(data.sources);
      } catch (error) {
        console.error('Error fetching topics:', error);
        setError('Failed to load topics');
        setTopics([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTopics();
  }, []);

  const handleChange = (event: SelectChangeEvent) => {
    const topic = event.target.value;
    setSelectedTopic(topic);
    onTopicChange(topic);
  };

  return (
    <FormControl fullWidth sx={{ mb: 2 }}>
      <InputLabel>Topic</InputLabel>
      <Select
        value={selectedTopic}
        label="Topic"
        onChange={handleChange}
        error={!!error}
        disabled={isLoading}
      >
        {isLoading ? (
          <MenuItem value="" disabled>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CircularProgress size={20} />
              Loading topics...
            </Box>
          </MenuItem>
        ) : (
          Array.isArray(topics) && topics.map((topic) => (
            <MenuItem key={topic} value={topic}>
              {topic}
            </MenuItem>
          ))
        )}
      </Select>
    </FormControl>
  );
} 
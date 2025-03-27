import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent } from '@mui/material';
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

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await fetch('/api/topics');
        if (!response.ok) {
          throw new Error('Failed to fetch topics');
        }
        const data: TopicsResponse = await response.json();
        
        // Validate that we received an array of sources
        if (!data.sources || !Array.isArray(data.sources)) {
          throw new Error('Invalid topics data received');
        }
        
        setTopics(data.sources);
      } catch (error) {
        console.error('Error fetching topics:', error);
        setError('Failed to load topics');
        setTopics([]); // Ensure topics is at least an empty array
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
      <InputLabel>Topics</InputLabel>
      <Select
        value={selectedTopic}
        label="Topics"
        onChange={handleChange}
        error={!!error}
      >
        {Array.isArray(topics) && topics.map((topic) => (
          <MenuItem key={topic} value={topic}>
            {topic}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
} 
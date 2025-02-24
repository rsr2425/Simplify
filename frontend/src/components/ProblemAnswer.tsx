import { TextField, Box, Typography } from '@mui/material';
import { Problem } from '../types/Problem';

interface ProblemAnswerProps {
  problem: Problem;
  index: number;
  onAnswerChange: (index: number, answer: string) => void;
}

function ProblemAnswer({ problem, index, onAnswerChange }: ProblemAnswerProps) {
  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="h6" sx={{ mb: 1 }}>
        Question {index + 1}:
      </Typography>
      <Typography sx={{ mb: 2 }}>{problem.question}</Typography>
      <TextField
        fullWidth
        multiline
        rows={3}
        label="Your Answer"
        value={problem.userAnswer || ''}
        onChange={(e) => onAnswerChange(index, e.target.value)}
        variant="outlined"
      />
    </Box>
  );
}

export default ProblemAnswer; 
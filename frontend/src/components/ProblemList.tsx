import { List, ListItem, Paper, Typography } from '@mui/material';

interface ProblemListProps {
  problems: string[];
}

function ProblemList({ problems }: ProblemListProps) {
  if (problems.length === 0) return null;

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Generated Problems
      </Typography>
      <List>
        {problems.map((problem, index) => (
          <ListItem key={index}>
            {index + 1}. {problem}
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}

export default ProblemList;
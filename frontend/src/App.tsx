import { Container, CssBaseline, ThemeProvider, createTheme, Button, Box, Typography, Alert } from '@mui/material';
import Header from './components/Header';
import DocumentInput from './components/DocumentInput';
import QuizGenerator from './components/QuizGenerator';
import ProblemAnswer from './components/ProblemAnswer';
import { useState } from 'react';
import { Problem } from './types/Problem';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

interface ProblemWithFeedback extends Problem {
  feedback?: string;
}

function App() {
  const [problems, setProblems] = useState<ProblemWithFeedback[]>([]);
  const [quizTopic, setQuizTopic] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const handleProblemsGenerated = (newProblems: string[], query: string) => {
    const problemObjects = newProblems.map(question => ({ question }));
    setProblems(problemObjects);
    setQuizTopic(query);
  };

  const handleAnswerChange = (index: number, answer: string) => {
    setProblems(prevProblems => {
      const newProblems = [...prevProblems];
      newProblems[index] = { ...newProblems[index], userAnswer: answer };
      return newProblems;
    });
  };

  const handleSubmit = async () => {
    try {
      setError(null);
      
      // Validate that all problems have answers
      const unansweredProblems = problems.some(p => !p.userAnswer);
      if (unansweredProblems) {
        setError('Please answer all questions before submitting');
        return;
      }

      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_query: quizTopic,
          problems: problems.map(p => p.question),
          user_answers: problems.map(p => p.userAnswer as string) // We can safely cast since we validated above
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || 'Failed to submit answers');
      }

      const data = await response.json();
      
      setProblems(prevProblems => 
        prevProblems.map((problem, index) => ({
          ...problem,
          feedback: data.feedback[index]
        }))
      );
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An error occurred');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Header />
        <DocumentInput />
        <QuizGenerator onProblemsGenerated={handleProblemsGenerated} />
        
        {error && (
          <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
            {error}
          </Alert>
        )}

        {problems.map((problem, index) => (
          <Box key={index} sx={{ mb: 4 }}>
            <ProblemAnswer
              problem={problem}
              index={index}
              onAnswerChange={handleAnswerChange}
            />
            {problem.feedback && (
              <Box sx={{ mt: 2, pl: 2, borderLeft: 3, borderColor: 'primary.main' }}>
                <Typography variant="h6" color="primary" gutterBottom>
                  Feedback:
                </Typography>
                <Typography>
                  {problem.feedback}
                </Typography>
              </Box>
            )}
          </Box>
        ))}

        {problems.length > 0 && (
          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={handleSubmit}
            >
              Submit for Feedback
            </Button>
          </Box>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
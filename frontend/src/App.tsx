import { Container, CssBaseline, ThemeProvider, createTheme, Button, Box, Typography, Alert, CircularProgress, Grid } from '@mui/material';
import Header from './components/Header';
import DocumentInput from './components/DocumentInput';
import QuizGenerator from './components/QuizGenerator';
import ProblemAnswer from './components/ProblemAnswer';
import Topics from './components/Topics';
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
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState<string>('');

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

  const handleTopicChange = (topic: string) => {
    setSelectedTopic(topic);
  };

  const handleSubmit = async () => {
    try {
      setError(null);
      setIsSubmitting(true);
      
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
          selected_topic: selectedTopic,
          problems: problems.map(p => p.question),
          user_answers: problems.map(p => p.userAnswer as string)
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
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Header />
        <DocumentInput />
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} md={4}>
            <Topics onTopicChange={handleTopicChange} />
          </Grid>
          <Grid item xs={12} md={8}>
            <QuizGenerator onProblemsGenerated={handleProblemsGenerated} />
          </Grid>
        </Grid>

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
        
        {error && (
          <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
            {error}
          </Alert>
        )}

        {problems.length > 0 && (
          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2 }}>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={handleSubmit}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Submitting...' : 'Submit for Feedback'}
            </Button>
            {isSubmitting && <CircularProgress size={24} />}
          </Box>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
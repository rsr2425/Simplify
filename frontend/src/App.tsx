import { Container, CssBaseline, ThemeProvider, createTheme, Button, Box, Typography, Alert, CircularProgress, Grid } from '@mui/material';
import Header from './components/Header';
import DocumentInput from './components/DocumentInput';
import QuizGenerator from './components/QuizGenerator';
import ProblemAnswer from './components/ProblemAnswer';
import Topics from './components/Topics';
import { useState } from 'react';
import { Problem } from './types/Problem';
import './styles/global.css';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    background: {
      default: '#1a1a1a',
      paper: '#242424',
    },
    text: {
      primary: '#ffffff',
      secondary: 'rgba(255, 255, 255, 0.7)',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundImage: `
            linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px)
          `,
          backgroundSize: '20px 20px',
          backgroundPosition: '-1px -1px',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
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
      <Container 
        maxWidth="md" 
        sx={{ 
          py: 4,
          '& .MuiPaper-root': {
            backgroundColor: 'background.paper',
            backdropFilter: 'blur(10px)',
            borderRadius: 2,
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          },
        }}
      >
        <Header />
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} md={4}>
            <Topics onTopicChange={handleTopicChange} />
          </Grid>
          <Grid item xs={12} md={8}>
            <QuizGenerator onProblemsGenerated={handleProblemsGenerated} />
          </Grid>
        </Grid>
        <DocumentInput />

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
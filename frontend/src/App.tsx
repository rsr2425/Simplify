import { Container, CssBaseline, ThemeProvider, createTheme, Button, Box } from '@mui/material';
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

function App() {
  const [problems, setProblems] = useState<Problem[]>([]);

  const handleProblemsGenerated = (newProblems: string[]) => {
    const problemObjects = newProblems.map(question => ({ question }));
    setProblems(problemObjects);
  };

  const handleAnswerChange = (index: number, answer: string) => {
    setProblems(prevProblems => {
      const newProblems = [...prevProblems];
      newProblems[index] = { ...newProblems[index], userAnswer: answer };
      return newProblems;
    });
  };

  const handleSubmit = () => {
    // Here you can add the logic to handle the submission
    // For now, we'll just log the answers
    console.log('Submitted answers:', problems.map(p => ({
      question: p.question,
      answer: p.userAnswer
    })));
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Header />
        <DocumentInput />
        <QuizGenerator onProblemsGenerated={handleProblemsGenerated} />
        {problems.map((problem, index) => (
          <ProblemAnswer
            key={index}
            problem={problem}
            index={index}
            onAnswerChange={handleAnswerChange}
          />
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
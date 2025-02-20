import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import Header from './components/Header';
import DocumentInput from './components/DocumentInput';
import QuizGenerator from './components/QuizGenerator';
import ProblemList from './components/ProblemList';
import { useState } from 'react';

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
  const [problems, setProblems] = useState<string[]>([]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Header />
        <DocumentInput />
        <QuizGenerator onProblemsGenerated={setProblems} />
        <ProblemList problems={problems} />
      </Container>
    </ThemeProvider>
  );
}

export default App;
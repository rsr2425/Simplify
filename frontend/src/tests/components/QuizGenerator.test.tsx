import { render, screen, fireEvent } from '@testing-library/react';
import QuizGenerator from '../../components/QuizGenerator';

describe('QuizGenerator', () => {
  const mockOnProblemsGenerated = jest.fn();

  beforeEach(() => {
    global.fetch = jest.fn();
    mockOnProblemsGenerated.mockClear();
  });

  test('generates problems when button is clicked', async () => {
    const mockProblems = ['Problem 1', 'Problem 2'];
    const mockFetch = global.fetch as jest.Mock;
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ Problems: mockProblems }),
    });

    render(<QuizGenerator onProblemsGenerated={mockOnProblemsGenerated} />);
    
    const input = screen.getByLabelText('Quiz topic?');
    const button = screen.getByText('Generate');
    
    await fireEvent.change(input, { target: { value: 'React' } });
    await fireEvent.click(button);
    
    expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/problems/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_query: 'React' }),
    });
    expect(mockOnProblemsGenerated).toHaveBeenCalledWith(mockProblems);
  });
});
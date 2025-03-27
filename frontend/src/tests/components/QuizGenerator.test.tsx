import { render, screen, fireEvent, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import QuizGenerator from '../../components/QuizGenerator';

describe('QuizGenerator', () => {
  const mockFetch = jest.fn();
  const mockOnProblemsGenerated = jest.fn();
  global.fetch = mockFetch;
  
  beforeEach(() => {
    mockFetch.mockClear();
    mockOnProblemsGenerated.mockClear();
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ Problems: [] })
    });
  });

  test('generates problems when button is clicked', async () => {
    render(<QuizGenerator onProblemsGenerated={mockOnProblemsGenerated} />);
    
    const input = screen.getByLabelText('Quiz focus?');
    const button = screen.getByText('Generate');
    
    await act(async () => {
      await fireEvent.change(input, { target: { value: 'React' } });
      await fireEvent.click(button);
    });
    
    expect(mockFetch).toHaveBeenCalledWith('/api/problems/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_query: 'React' }),
    });
  });
});
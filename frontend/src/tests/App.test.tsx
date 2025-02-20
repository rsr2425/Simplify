import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

describe('App', () => {
  test('renders main components', () => {
    render(<App />);
    
    // Check for title
    expect(screen.getByText('Simplify')).toBeInTheDocument();
    
    // Check for input fields
    expect(screen.getByLabelText('Source Documentation')).toBeInTheDocument();
    expect(screen.getByLabelText('Quiz topic?')).toBeInTheDocument();
    
    // Check for buttons
    expect(screen.getByText('Pull Source Docs')).toBeInTheDocument();
    expect(screen.getByText('Generate')).toBeInTheDocument();
  });
});
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from '../App';

describe('App', () => {
  test('renders main components', () => {
    render(<App />);
    
    // Check for title
    expect(screen.getByText('SimpliFi')).toBeInTheDocument();
    
    // Check for input fields
    expect(screen.getByLabelText('Source Documentation')).toBeInTheDocument();
    expect(screen.getByLabelText('Quiz focus?')).toBeInTheDocument();
    
    // Check for buttons
    expect(screen.getByText('Scan')).toBeInTheDocument();
    expect(screen.getByText('Generate')).toBeInTheDocument();
  });
});
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from '../App';

describe('App', () => {
  test('renders main components', () => {
    render(<App />);
    
    // Check for title
    expect(screen.getByText('SimpliFi')).toBeInTheDocument();
    
    // Check for main button
    expect(screen.getByText('Add New Documentation')).toBeInTheDocument();
    expect(screen.getByText('Generate')).toBeInTheDocument();
  });

  test('opens modal with form fields when Add New Documentation is clicked', async () => {
    render(<App />);
    
    const addButton = screen.getByText('Add New Documentation');
    await userEvent.click(addButton);
    
    // Check modal content
    expect(screen.getByLabelText('Source Documentation URL')).toBeInTheDocument();
    expect(screen.getByLabelText('Topic Name')).toBeInTheDocument();
    expect(screen.getByText('Cancel')).toBeInTheDocument();
    expect(screen.getByText('Confirm')).toBeInTheDocument();
  });

  test('confirm button is disabled when fields are empty', async () => {
    render(<App />);
    
    const addButton = screen.getByText('Add New Documentation');
    await userEvent.click(addButton);
    
    const confirmButton = screen.getByText('Confirm');
    expect(confirmButton).toBeDisabled();
  });
});
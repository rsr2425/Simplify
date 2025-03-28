import { render, screen, fireEvent, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import DocumentInput from '../../components/DocumentInput';

describe('DocumentInput', () => {
  const mockFetch = jest.fn();
  global.fetch = mockFetch;
  
  beforeEach(() => {
    mockFetch.mockClear();
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({}) });
  });

  test('submits URL and shows success message while keeping URL in input', async () => {
    render(<DocumentInput />);
    
    const input = screen.getByLabelText('Source Documentation');
    const button = screen.getByText('Scan');
    
    await act(async () => {
      await fireEvent.change(input, { target: { value: 'https://example.com' } });
      await fireEvent.click(button);
    });
    
    expect(mockFetch).toHaveBeenCalledWith('/api/ingest/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: 'https://example.com' }),
    });

    // Check if success message is shown
    expect(screen.getByText('Source documentation imported successfully!')).toBeInTheDocument();
    
    // Verify URL is still in the input
    expect(input).toHaveValue('https://example.com');
  });

  test('hides success message when starting to type new URL', async () => {
    render(<DocumentInput />);
    
    // First submit a URL
    const input = screen.getByLabelText('Source Documentation');
    const button = screen.getByText('Scan');
    
    await act(async () => {
      await fireEvent.change(input, { target: { value: 'https://example.com' } });
      await fireEvent.click(button);
    });

    // Verify success message is shown
    expect(screen.getByText('Source documentation imported successfully!')).toBeInTheDocument();

    // Start typing new URL
    await act(async () => {
      await fireEvent.change(input, { target: { value: 'https://new' } });
    });

    // Verify success message is hidden
    expect(screen.queryByText('Source documentation imported successfully!')).not.toBeInTheDocument();
  });
});
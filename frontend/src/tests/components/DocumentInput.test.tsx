import { render, screen, fireEvent } from '@testing-library/react';
import DocumentInput from '../../components/DocumentInput';

describe('DocumentInput', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  test('submits URL when button is clicked', async () => {
    const mockFetch = global.fetch as jest.Mock;
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ status: 'received' }),
    });

    render(<DocumentInput />);
    
    const input = screen.getByLabelText('Source Documentation');
    const button = screen.getByText('Pull Source Docs');
    
    await fireEvent.change(input, { target: { value: 'https://example.com' } });
    await fireEvent.click(button);
    
    expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/crawl/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: 'https://example.com' }),
    });
  });
});
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

  test('submits URL when button is clicked', async () => {
    render(<DocumentInput />);
    
    const input = screen.getByLabelText('Source Documentation');
    const button = screen.getByText('Pull Source Docs');
    
    await act(async () => {
      await fireEvent.change(input, { target: { value: 'https://example.com' } });
      await fireEvent.click(button);
    });
    
    expect(mockFetch).toHaveBeenCalledWith('/api/crawl/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: 'https://example.com' }),
    });
  });
});
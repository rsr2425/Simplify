import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Topics from '../../components/Topics';

describe('Topics Component', () => {
  const mockOnTopicChange = jest.fn();
  const mockFetch = jest.fn();
  global.fetch = mockFetch;

  beforeEach(() => {
    jest.clearAllMocks();
    mockFetch.mockClear();
  });

  it('shows loading state initially', () => {
    render(<Topics onTopicChange={mockOnTopicChange} />);
    
    expect(screen.getByLabelText('Topic')).toBeDisabled();
    expect(screen.getByText('Loading topics...')).toBeInTheDocument();
  });

  it('displays topics after successful fetch', async () => {
    const mockTopics = { sources: ['Topic 1', 'Topic 2', 'Topic 3'] };
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockTopics),
      })
    );

    render(<Topics onTopicChange={mockOnTopicChange} />);

    // Wait for loading to finish
    await waitFor(() => {
      expect(screen.queryByText('Loading topics...')).not.toBeInTheDocument();
    });

    // Open the dropdown
    fireEvent.mouseDown(screen.getByLabelText('Topic'));

    // Check if all topics are rendered
    mockTopics.sources.forEach(topic => {
      expect(screen.getByText(topic)).toBeInTheDocument();
    });
  });

  it('handles API error correctly', async () => {
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
        status: 500,
      })
    );

    render(<Topics onTopicChange={mockOnTopicChange} />);

    await waitFor(() => {
      expect(screen.queryByText('Loading topics...')).not.toBeInTheDocument();
    });

    const select = screen.getByLabelText('Topic');
    expect(select).toHaveAttribute('aria-invalid', 'true');
  });

  it('calls onTopicChange when topic is selected', async () => {
    const mockTopics = { sources: ['Topic 1', 'Topic 2'] };
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockTopics),
      })
    );

    render(<Topics onTopicChange={mockOnTopicChange} />);

    // Wait for loading to finish
    await waitFor(() => {
      expect(screen.queryByText('Loading topics...')).not.toBeInTheDocument();
    });

    // Open the dropdown
    fireEvent.mouseDown(screen.getByLabelText('Topic'));
    
    // Select a topic
    fireEvent.click(screen.getByText('Topic 1'));

    expect(mockOnTopicChange).toHaveBeenCalledWith('Topic 1');
  });

  it('handles malformed API response correctly', async () => {
    const malformedResponse = { wrongKey: [] };
    mockFetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(malformedResponse),
      })
    );

    render(<Topics onTopicChange={mockOnTopicChange} />);

    await waitFor(() => {
      expect(screen.queryByText('Loading topics...')).not.toBeInTheDocument();
    });

    const select = screen.getByLabelText('Topic');
    expect(select).toHaveAttribute('aria-invalid', 'true');
  });

  it('handles network errors correctly', async () => {
    mockFetch.mockImplementationOnce(() =>
      Promise.reject(new Error('Network error'))
    );

    render(<Topics onTopicChange={mockOnTopicChange} />);

    await waitFor(() => {
      expect(screen.queryByText('Loading topics...')).not.toBeInTheDocument();
    });

    const select = screen.getByLabelText('Topic');
    expect(select).toHaveAttribute('aria-invalid', 'true');
  });
}); 
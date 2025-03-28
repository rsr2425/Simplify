import os
import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from scrapy.http import Response, Request
from backend.app.crawler import WebsiteSpider, DomainCrawler

@pytest.fixture
def sample_html():
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content.</p>
            </main>
        </body>
    </html>
    """

@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary directory for test outputs"""
    return str(tmp_path / "test_crawled_content")

def test_website_spider_initialization():
    """Test WebsiteSpider initialization with correct parameters"""
    start_url = "https://example.com"
    output_dir = "test_output"
    
    spider = WebsiteSpider(start_url=start_url, output_dir=output_dir)
    
    assert spider.start_urls == [start_url]
    assert spider.allowed_domains == ["example.com"]
    assert spider.output_dir == output_dir
    assert len(spider.rules) == 1

def test_parse_item_with_main_content(sample_html, output_dir):
    """Test parsing a page with main content section"""
    start_url = "https://example.com"
    spider = WebsiteSpider(start_url=start_url, output_dir=output_dir)
    
    # Create a mock response
    mock_response = Mock(spec=Response)
    mock_response.url = "https://example.com/test"
    mock_response.body = sample_html.encode('utf-8')
    
    # Process the mock response
    spider.parse_item(mock_response)
    
    # Check if file was created and contains correct content
    files = os.listdir(output_dir)
    assert len(files) == 1
    
    with open(os.path.join(output_dir, files[0]), 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Test Page" in content
        assert "Main Content" in content
        assert "This is the main content" in content
        assert "URL: https://example.com/test" in content

def test_parse_item_without_main_content(output_dir):
    """Test parsing a page without main content section"""
    html_without_main = """
    <html>
        <head><title>No Main Page</title></head>
        <body>
            <div>Some body content</div>
        </body>
    </html>
    """
    
    start_url = "https://example.com"
    spider = WebsiteSpider(start_url=start_url, output_dir=output_dir)
    
    mock_response = Mock(spec=Response)
    mock_response.url = "https://example.com/no-main"
    mock_response.body = html_without_main.encode('utf-8')
    
    spider.parse_item(mock_response)
    
    files = os.listdir(output_dir)
    assert len(files) == 1
    
    with open(os.path.join(output_dir, files[0]), 'r', encoding='utf-8') as f:
        content = f.read()
        assert "No Main Page" in content
        assert "Some body content" in content

def test_domain_crawler_initialization():
    """Test DomainCrawler initialization"""
    start_url = "https://example.com"
    output_dir = "test_output"
    
    crawler = DomainCrawler(start_url=start_url, output_dir=output_dir)
    
    assert crawler.start_url == start_url
    assert crawler.domain == "example.com"
    assert crawler.output_dir == output_dir
    assert crawler.settings.get('BOT_NAME') == "website_crawler"
    assert crawler.settings.get('ROBOTSTXT_OBEY') is True
    assert crawler.settings.get('CONCURRENT_REQUESTS') == 16
    assert crawler.settings.get('DOWNLOAD_DELAY') == 1

@patch('backend.app.crawler.CrawlerProcess')
def test_domain_crawler_start(mock_crawler_process):
    """Test starting the domain crawler"""
    start_url = "https://example.com"
    output_dir = "test_output"
    
    crawler = DomainCrawler(start_url=start_url, output_dir=output_dir)
    crawler.start()
    
    # Verify that CrawlerProcess was instantiated and crawl was started
    mock_crawler_process.assert_called_once_with(crawler.settings)
    mock_crawler_process.return_value.crawl.assert_called_once()
    mock_crawler_process.return_value.start.assert_called_once()

def test_output_directory_creation():
    """Test that output directory is created if it doesn't exist"""
    start_url = "https://example.com"
    output_dir = "test_output_dir"
    
    # Ensure directory doesn't exist
    if os.path.exists(output_dir):
        os.rmdir(output_dir)
    
    crawler = DomainCrawler(start_url=start_url, output_dir=output_dir)
    assert os.path.exists(output_dir)
    
    # Cleanup
    os.rmdir(output_dir) 
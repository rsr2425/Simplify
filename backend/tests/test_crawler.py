import pytest
import os
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from scrapy.http import Response, Request, TextResponse
from backend.app.crawler import DomainCrawler, WebsiteSpider


@pytest.fixture
def sample_html():
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content of the page.</p>
            </main>
        </body>
    </html>
    """


@pytest.fixture
def crawler():
    return DomainCrawler("https://example.com", output_dir="test_output")


@pytest.fixture
def spider():
    return WebsiteSpider(start_url="https://example.com", output_dir="test_output")


# def test_crawler_initialization(crawler):
#     assert crawler.start_url == "https://example.com"
#     assert crawler.domain == "example.com"
#     assert crawler.output_dir == "test_output"
#     assert os.path.exists("test_output")

#     # Test Scrapy settings
#     assert crawler.settings.get('BOT_NAME') == 'website_crawler'
#     assert crawler.settings.get('ROBOTSTXT_OBEY') is True
#     assert crawler.settings.get('DOWNLOAD_DELAY') == 1


def create_response(url, body):
    request = Request(url=url)
    return TextResponse(
        url=url, body=body.encode("utf-8"), encoding="utf-8", request=request
    )


# def test_spider_parse_with_main_content(spider, sample_html):
#     url = "https://example.com/test"
#     response = create_response(url, sample_html)

#     # Process the page
#     list(spider.parse_item(response))

#     # Check if file was created
#     files = os.listdir(spider.output_dir)
#     assert len(files) == 1

#     # Read the saved file
#     with open(os.path.join(spider.output_dir, files[0]), 'r', encoding='utf-8') as f:
#         content = f.read()

#     # Verify content
#     assert "URL: https://example.com/test" in content
#     assert "Title: Test Page" in content
#     assert "Main Content" in content
#     assert "This is the main content of the page." in content

# def test_spider_parse_without_main_content(spider):
#     html_without_main = """
#     <html>
#         <head><title>No Main</title></head>
#         <body>
#             <div>Some body content</div>
#         </body>
#     </html>
#     """

#     url = "https://example.com/no-main"
#     response = create_response(url, html_without_main)

#     # Process the page
#     list(spider.parse_item(response))

#     files = os.listdir(spider.output_dir)
#     assert len(files) == 1

#     with open(os.path.join(spider.output_dir, files[0]), 'r', encoding='utf-8') as f:
#         content = f.read()

#     assert "URL: https://example.com/no-main" in content
#     assert "Title: No Main" in content
#     assert "Some body content" in content

# def test_spider_parse_with_invalid_html(spider):
#     invalid_html = "<invalid><<html>"
#     url = "https://example.com/invalid"
#     response = create_response(url, invalid_html)

#     # Process should not raise an exception
#     list(spider.parse_item(response))

#     # Should still create a file
#     files = os.listdir(spider.output_dir)
#     assert len(files) == 1

# @patch('scrapy.crawler.CrawlerProcess')
# def test_start_crawling(mock_crawler_process_class, crawler):
#     # Configure the mock
#     mock_process = Mock()
#     mock_crawler_process_class.return_value = mock_process

#     # Start crawling
#     crawler.start()

#     # Verify process was created with correct settings
#     mock_crawler_process_class.assert_called_once_with(crawler.settings)

#     # Verify crawl method was called
#     mock_process.crawl.assert_called_once()
#     mock_process.start.assert_called_once()


@pytest.fixture(autouse=True)
def cleanup():
    # Setup - nothing needed
    yield
    # Cleanup after each test
    if os.path.exists("test_output"):
        for file in os.listdir("test_output"):
            os.remove(os.path.join("test_output", file))
        os.rmdir("test_output")

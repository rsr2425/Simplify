import os
import re
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class WebsiteSpider(CrawlSpider):
    name = "website_spider"

    def __init__(self, start_url, output_dir, *args, **kwargs):
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.output_dir = output_dir

        # Define rules for link extraction
        self.rules = (
            Rule(
                LinkExtractor(allow_domains=self.allowed_domains),
                callback="parse_item",
                follow=True,
            ),
        )

        super().__init__(*args, **kwargs)

    def parse_item(self, response):
        try:
            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(response.body, "html.parser")

            # Extract the title
            title = soup.title.string if soup.title else "No Title"

            # Clean the filename
            filename = re.sub(r"[^\w\-_]", "_", title) + ".txt"
            filepath = os.path.join(self.output_dir, filename)

            # Extract main content
            main_content = (
                soup.find("main")
                or soup.find("article")
                or soup.find("div", class_="content")
            )

            # If we found main content, extract the text
            if main_content:
                text_content = main_content.get_text(separator="\n", strip=True)
            else:
                # Fallback to body text
                text_content = (
                    soup.body.get_text(separator="\n", strip=True)
                    if soup.body
                    else "No content"
                )
                logger.warning(
                    f"No main content found for {response.url}, falling back to body text"
                )

            # Save the extracted content
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"URL: {response.url}\n")
                f.write(f"Title: {title}\n\n")
                f.write(text_content)

            logger.info(f"Saved content from {response.url} to {filepath}")

        except Exception as e:
            logger.error(f"Error processing {response.url}: {e}", exc_info=True)


class DomainCrawler:
    def __init__(self, start_url, output_dir="crawled_content"):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")

        # Configure Scrapy settings
        self.settings = get_project_settings()
        self.settings.update(
            {
                "BOT_NAME": "website_crawler",
                "ROBOTSTXT_OBEY": True,
                "CONCURRENT_REQUESTS": 16,
                "DOWNLOAD_DELAY": 1,
                "COOKIES_ENABLED": False,
                "USER_AGENT": "Mozilla/5.0 (compatible; SimplifyCrawler/1.0)",
            }
        )

    def start(self):
        """Start the crawling process"""
        logger.info(f"Starting crawl from {self.start_url}")

        process = CrawlerProcess(self.settings)
        process.crawl(
            WebsiteSpider, start_url=self.start_url, output_dir=self.output_dir
        )
        process.start()

        logger.info("\nCrawl completed!")
        logger.info(f"Content saved to: {os.path.abspath(self.output_dir)}")

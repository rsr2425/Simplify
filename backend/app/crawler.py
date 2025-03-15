from spidy import crawler
import os
import re
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


class DomainCrawler:
    def __init__(self, start_url, output_dir="crawled_content"):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")

        # Initialize the crawler
        self.crawler = crawler.Crawler(
            start_url=start_url,
            max_pages=1000,
            timeout=10,
            delay=0.5,
            save_pages=True,
            save_path=output_dir,
            restrict_domain=True,
            verbose=True,
        )

        # Set custom handlers
        self.crawler.page_handler = self.process_page

    def process_page(self, url, content):
        """Custom page processor that extracts and saves content"""
        try:
            # Parse the HTML
            soup = BeautifulSoup(content, "html.parser")

            # Extract the title
            title = soup.title.string if soup.title else "No Title"

            # Clean the filename
            filename = re.sub(r"[^\w\-_]", "_", title) + ".txt"
            filepath = os.path.join(self.output_dir, filename)

            # Extract main content (this is just an example - adjust for your site)
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
                    f"No main content found for {url}, falling back to body text"
                )

            # Save the extracted content
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"URL: {url}\n")
                f.write(f"Title: {title}\n\n")
                f.write(text_content)

            logger.info(f"Saved content from {url} to {filepath}")

        except Exception as e:
            logger.error(f"Error processing {url}: {e}", exc_info=True)

        return content  # Return the original content for the crawler to continue

    def start(self):
        """Start the crawling process"""
        logger.info(f"Starting crawl from {self.start_url}")
        self.crawler.crawl()

        # Print summary
        logger.info("\nCrawl completed!")
        logger.info(f"Pages crawled: {len(self.crawler.links_crawled)}")
        logger.info(f"Content saved to: {os.path.abspath(self.output_dir)}")

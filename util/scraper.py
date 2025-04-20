import os
import time
from dataclasses import dataclass
from typing import List, Optional, Set
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from functools import wraps
import backoff


@dataclass
class ScraperConfig:
    wait_timeout: int = 30
    download_timeout: int = 60
    retry_attempts: int = 3
    headless: bool = True
    button_id: str = "pdfdoc"


def setup_chrome_options(download_folder: str, headless: bool = True) -> Options:
    """Configure Chrome options for the WebDriver."""
    chrome_options = Options()
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    return chrome_options


def retry_on_exception(retries: int = 3):
    """Decorator for retrying operations that might fail."""

    def decorator(func):
        @backoff.on_exception(backoff.expo, Exception, max_tries=retries)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


class PDFDownloader:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.driver: Optional[WebDriver] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        """Clean up WebDriver resources."""
        if self.driver:
            logging.info("Quitting PDFDownloader WebDriver.")
            self.driver.quit()
            self.driver = None

    def initialize_driver(self, download_folder: str):
        """Initialize the WebDriver with proper configuration."""
        if not self.driver:  # Only initialize if not already done
            logging.info("Initializing PDFDownloader WebDriver.")
            options = setup_chrome_options(download_folder, self.config.headless)
            self.driver = webdriver.Chrome(options=options)
        else:
            logging.debug("PDFDownloader WebDriver already initialized.")

    def wait_for_download(
        self, download_folder: str, files_before: Set[str]
    ) -> Optional[str]:
        """Wait for download to complete and return the downloaded file path."""
        start_time = time.time()
        while time.time() - start_time < self.config.download_timeout:
            files_after = set(os.listdir(download_folder))
            new_files = files_after - files_before

            for file in new_files:
                if file.lower().endswith(".pdf") and not file.lower().endswith(
                    ".crdownload"
                ):
                    file_path = os.path.join(download_folder, file)
                    # Ensure file is completely written
                    if self._is_file_ready(file_path):
                        logging.info(f"Detected new file: {file_path}")
                        return file_path
                    else:
                        logging.debug(f"File not ready yet: {file_path}")

            time.sleep(1)
        logging.warning(f"Download timeout reached for folder: {download_folder}")
        return None

    @staticmethod
    def _is_file_ready(file_path: str, timeout: int = 5) -> bool:
        """Check if file is completely written and ready."""
        start_time = time.time()
        last_size = -1
        while time.time() - start_time < timeout:
            try:
                current_size = os.path.getsize(file_path)
                if (
                    current_size == last_size and current_size > 0
                ):  # Check if size stopped changing
                    # Try to open file to verify it's not locked
                    with open(file_path, "rb") as _:
                        return True
                last_size = current_size
            except (IOError, PermissionError, FileNotFoundError):
                # File might not exist yet or be locked
                pass
            except Exception as e:
                logging.error(
                    f"Unexpected error checking file readiness for {file_path}: {e}"
                )
                return False  # Avoid infinite loop on unexpected errors
            time.sleep(0.5)
        logging.warning(f"File readiness check timed out for: {file_path}")
        return False

    @retry_on_exception()
    def download_pdf(self, url: str, download_folder: str) -> Optional[str]:
        """Download PDF from the given URL."""
        os.makedirs(download_folder, exist_ok=True)

        # Initialize driver if it hasn't been initialized yet
        self.initialize_driver(download_folder)
        if not self.driver:  # Check if initialization failed
            logging.error("WebDriver not initialized for PDF download.")
            return None

        logging.info(f"Navigating to URL for PDF download: {url}")
        self.driver.get(url)
        files_before = set(os.listdir(download_folder))
        logging.debug(f"Files before download in {download_folder}: {files_before}")

        try:
            logging.info(f"Waiting for download button (ID: {self.config.button_id})")
            button = WebDriverWait(self.driver, self.config.wait_timeout).until(
                EC.element_to_be_clickable((By.ID, self.config.button_id))
            )
            logging.info("Download button found, clicking...")
            button.click()
            logging.info("Waiting for download to complete...")
            return self.wait_for_download(download_folder, files_before)

        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Failed to find or click download button on {url}: {str(e)}")
            return None
        except Exception as e:
            logging.error(
                f"An unexpected error occurred during PDF download from {url}: {e}"
            )
            return None


class LinkExtractor:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.driver: Optional[WebDriver] = None

    def __enter__(self):
        """Initialize WebDriver when entering the 'with' block."""
        self.initialize_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up WebDriver when exiting the 'with' block."""
        self.cleanup()

    def initialize_driver(self):
        """Initialize WebDriver for link extraction."""
        if not self.driver:  # Initialize only if it doesn't exist
            logging.info("Initializing LinkExtractor WebDriver.")
            options = Options()
            if self.config.headless:
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--start-maximized")  # Often helpful even in headless
            self.driver = webdriver.Chrome(options=options)
        else:
            logging.debug("LinkExtractor WebDriver already initialized.")

    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            logging.info("Quitting LinkExtractor WebDriver.")
            self.driver.quit()
            self.driver = None

    @retry_on_exception()
    def extract_links(self, url: str) -> List[str]:
        """Extract links from the specified URL using the existing driver."""
        if not self.driver:
            logging.error("WebDriver not initialized. Call within a 'with' block.")
            return []

        try:
            logging.info(f"Navigating to URL for link extraction: {url}")
            self.driver.get(url)

            # Wait for at least one result title link to be present
            WebDriverWait(self.driver, self.config.wait_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.result_title a"))
            )

            links = []
            # Find elements again after waiting to ensure they are loaded
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.result_title a")
            logging.info(f"Found {len(elements)} potential links on {url}.")

            for element in elements:
                href = element.get_attribute("href")
                if href:
                    links.append(href)

            return links
        except TimeoutException:
            logging.warning(
                f"Timeout waiting for result titles on {url}. No links extracted."
            )
            return []
        except Exception as e:
            logging.error(
                f"An unexpected error occurred during link extraction from {url}: {e}"
            )
            return []  # Return empty list on error


def main():
    config = ScraperConfig(headless=True)  # Set headless mode here if desired
    base_url = "https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%202020&pagenum="
    download_folder = "E:\\Programming\\Agentic\\Legal Assistant\\docs" # Change download path accordingly
    num_pages_to_scrape = 10  # Define how many pages

    all_links = []

    logging.info("Starting link extraction...")
    try:
        with LinkExtractor(config) as extractor:
            for i in range(num_pages_to_scrape):  # Loop from 0 to 9
                target_url_with_page = f"{base_url}{i}"
                logging.info(f"Extracting links from page {i}: {target_url_with_page}")
                page_links = extractor.extract_links(target_url_with_page)
                if page_links:
                    all_links.extend(page_links)
                    logging.info(f"Extracted {len(page_links)} links from page {i}.")
                else:
                    logging.warning(f"No links found on page {i}.")
                    
    except Exception as e:
        logging.error(f"An error occurred during link extraction process: {e}")

    logging.info(f"Finished link extraction. Total links found: {len(all_links)}")

    if not all_links:
        logging.warning("No links were extracted. Skipping PDF download.")
        return

    logging.info("Starting PDF download process...")
    try:
        with PDFDownloader(config) as downloader:
            for i, link in enumerate(all_links, 1):
                logging.info(f"--- Downloading {i}/{len(all_links)}: {link} ---")
                pdf_path = downloader.download_pdf(link, download_folder)
                if pdf_path:
                    logging.info(f"Successfully downloaded to: {pdf_path}")
                else:
                    logging.error(f"Failed to download: {link}")

    except Exception as e:
        logging.error(f"An error occurred during the PDF download process: {e}")

    logging.info("Script finished.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()

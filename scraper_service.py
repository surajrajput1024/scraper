import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


class ScraperService:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()

    def get_page_content(self, url: str, retries=3, delay=2):
        """
        Fetches the page content using Selenium (to handle JS-rendered pages) with retries.
        """
        for attempt in range(retries):
            try:
                self.logger.info(f"Fetching URL: {url}")
                self.driver.get(url)
                
                # Waiting for the page to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "product-inner"))
                )
                return self.driver.page_source
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {e}")
                if attempt < retries - 1:
                    self.logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    self.logger.error(f"Failed to fetch {url} after {retries} attempts.")
                    return None          

    def extract_product_data(self, product_html, retries=3, delay=2):
        """
        Extracts product data from HTML, with retries in case of failure.
        """
        for attempt in range(retries):
            try:
                product_name = product_html.find('h2', class_='woo-loop-product__title')
                product_name = product_name.get_text(strip=True) if product_name else "Unnamed Product"

                product_price = product_html.find('span', class_='woocommerce-Price-amount')
                product_price = product_price.get_text(strip=True) if product_price else "Price Unavailable"

                product_link = product_html.find('a')
                product_link = product_link['href'] if product_link else None

                product_image = product_html.find('img')
                product_image = product_image['src'] if product_image else None

                return {
                    'product_title': product_name,
                    'price': product_price,
                    'link': product_link,
                    'image': product_image,
                }
            except Exception as e:
                self.logger.error(f"Error extracting product data: {e}")
                if attempt < retries - 1:
                    self.logger.info(f"Retrying extraction in {delay} seconds...")
                    time.sleep(delay)
                else:
                    self.logger.error(f"Failed to extract product data after {retries} attempts.")
                    return None

    def scrape(self, base_url: str, max_pages: int):
        """
        Scrapes products from a paginated e-commerce site.
        """
        all_scraped_data = []
        try:
            for page_number in range(1, max_pages + 1):
                page_url = f"{base_url}page/{page_number}/"
                self.logger.info(f"Processing page: {page_url}")

                page_content = self.get_page_content(page_url)
                if not page_content:
                    self.logger.error(f"No content retrieved from {page_url}")
                    continue

                soup = BeautifulSoup(page_content, 'html.parser')
                product_list = soup.find_all('div', class_='product-inner')

                if not product_list:
                    self.logger.warning(f"No products found on {page_url}")
                    continue

                self.logger.info(f"Found {len(product_list)} products on page {page_number}")

                for product_html in product_list:
                    product_data = self.extract_product_data(product_html)
                    if product_data:
                        all_scraped_data.append(product_data)
        finally:
            # Closing driver after scraping
            self.driver.quit()

        return all_scraped_data

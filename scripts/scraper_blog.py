from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

def extract_urls(url_list, timeout=30, max_pages=None):
    """Extracts URLs from a list of websites using Selenium and BeautifulSoup.

    Args:
        url_list (list): A list of URLs to scrape.
        timeout (int, optional): The maximum time to wait for elements to load
                                 (default: 10 seconds).
        max_pages (int, optional): The maximum number of pages to scrape
                                 (default: None, scrape all pages).

    Returns:
        list: A list of all extracted URLs from all provided URLs.
    """

    extracted_urls = []
    with tqdm(total=len(url_list), desc="Scraping blogpost URLs") as pbar:
        for url in url_list:
            extracted_urls.extend(extract_blog_posts_from_url(url, timeout, max_pages))
            pbar.update(1)

    return extracted_urls

def extract_data_from_urls(url_list):
    """Extracts data from a list of URLs.

    Args:
        url_list: A list of URLs to scrape.

    Returns:
        list: A list of dictionaries containing extracted data for each URL.
    """

    extracted_data = []
    total_urls = len(url_list)

    with tqdm(total=total_urls, desc="Extracting blogpost data") as pbar:
        for url in url_list:
            data = extract_content(url)
            extracted_data.append(data)
            pbar.update(1)

    return extracted_data

def extract_content(url):
    """Extracts title and content from a given URL based on specific HTML structure.

    Args:
        url: The URL to scrape.

    Returns:
        tuple: A tuple containing the extracted title and content.
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

    # Find the title element
    title_element = soup.find('h1', class_='entry-title')
    title = title_element.text.strip() if title_element else None

    # Find the content element, excluding the feedback container
    content_element = soup.find('div', class_='et_pb_post_content', exclude={'class': 'daexthefu-container'})
    content = content_element.text.strip() if content_element else None

    # Remove any content within the feedback container
    for feedback_container in soup.find_all('div', class_='daexthefu-container'):
        feedback_container.extract()

    # Find the content element again after removing feedback
    content_element = soup.find('div', class_='et_pb_post_content')
    content = content_element.text.strip() if content_element else None

    return title, content

def extract_blog_posts_from_url(url, timeout=30, max_pages=None):
    """Extracts URLs from a paginated website using Selenium and BeautifulSoup.

    Args:
        url (str): The base URL of the website to scrape.
        timeout (int, optional): The maximum time to wait for elements to load
                                 (default: 30 seconds).
        max_pages (int, optional): The maximum number of pages to scrape
                                 (default: None, scrape all pages).

    Returns:
        list: A list of all extracted URLs from all paginated pages.
    """

    extracted_urls = []
    current_page = 1


    # Create Firefox options object
    options = Options()

    # Enable incognito mode
    options.add_argument('-private')  # Flag for incognito in Firefox
    options.add_argument('--headless')  # Make the driver headless (opening the browser in the background)

    # Generate random user agent
    ua = UserAgent()
    user_agent = ua.random

    # Set user agent header
    options.set_preference('general.useragent.override', user_agent)

    # Suppress Selenium logging
    options.log_level = '3'  # Set logging level to 'severe' (equivalent to 3)

    # Choose the appropriate browser driver
    driver = webdriver.Firefox(options=options)  # Replace with 'Chrome' or your preferred driver

    while True:
        # Construct the current page URL
        page_url = f"{url}/page/{current_page}/?et_blog" if current_page > 1 else url

        # Open the current page
        driver.get(page_url)

        try:
            # Explicitly wait for specific element or condition to indicate page load
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "more-link"))  # Replace with relevant element
            )
        except TimeoutError:
            print(f"Timeout waiting for element on {page_url}")
            # Handle timeout gracefully (e.g., skip this page, retry)

        # Get the HTML content
        html_content = driver.page_source

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html5lib')  # Consider using 'html5lib' for better compatibility

        # Find all 'a' tags with specific class (adjust if needed)
        all_links = soup.find_all('a', class_='more-link')  # Example: Find by class

        # Extract URLs from the links on this page
        for link in all_links:
            href = link.get('href')
            if href:
                extracted_urls.append(href)

        # Check for next page link
        next_page_link = soup.find('a', class_='nextpostslink')

        # Break the loop if no next page or maximum pages reached
        if not next_page_link or (max_pages and current_page >= max_pages):
            break

        current_page += 1  # Move to the next page

    # Close the browser
    driver.quit()

    return extracted_urls

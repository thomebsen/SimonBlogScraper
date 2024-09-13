# Simons Japan Blog Post Scraper

## Overview

This Python script is designed to extract blog post titles and content from specified categories on Simon Japan's website, https://simonsjapan.dk/  

The generated output is a `.json` file for easy data analysis or further processing.

## Prerequisites

* Python 3.x
* Required Python packages (listed in `requirements.txt`)

## Installation

1. **Clone the repository:**
   ```
    git clone https://github.com/thomebsen/SimonBlogScraper
   ```
2. **Cd into the repository**
    ```
    cd SimonBlogScraper
    ```
3. **Install the required packages**
    ```
    pip install -r requirements.txt
    ```

## Usage
1. **Prepare the [sites_to_scrape](sites_to_scrape.csv) file:**
    * Add the URLs of the blog post categories you want to scrape, one per line.
2. **Run the script:**
    ```
    python program.py
    ```
The script will process each category and save the extracted data to a .json file named [extracted_blogpost_data.json](extracted_blogpost_data.json).

# Important Notes
* **Error Handling:** While the script is designed to be robust, it may encounter issues in certain scenarios (e.g., network errors, CAPTCHAs). Consider implementing additional error handling mechanisms for more reliable execution.

* **Performance Optimization:** For large-scale scraping, you might want to explore techniques like asynchronous requests or headless browsers to improve performance and avoid rate limiting.

* **Ethical Considerations:** Always respect the terms of service and robots.txt of the website you're scraping. Avoid excessive requests that could strain their servers or lead to account suspension.
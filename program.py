from scripts.url_extractor import extract_urls, extract_data_from_urls
import csv, os, json
import pandas as pd

timeout = 30

tracker_urls_pre = pd.read_csv(os.path.join(os.path.dirname(__file__), '', 'sites_to_scrape.csv'), sep=';')
tracker_urls_list = tracker_urls_pre.url


def program():
    print("XXXXXXXX [START] XXXXXXXX")
    print("Running...")
    print("Please have patience...")
    extracted_urls = extract_urls(tracker_urls_list)  # Scrape urls
    extracted_urls = list(dict.fromkeys(extracted_urls))  # Remove potential duplicates

    for url in extracted_urls:  # Save extracted blogposts to extracted_urls.csv
        with open('extracted_blogpost_urls.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['URL'])  # Header row
            for url in extracted_urls:
                writer.writerow([url])

    extracted_data = extract_data_from_urls(extracted_urls)

    print("Saving data to [extracted_data.json]...")
    with open('extracted_blogpost_data.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=4)
    print("XXXXXXXX [FINISHED] XXXXXXXX")

program()
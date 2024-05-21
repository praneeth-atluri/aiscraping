import csv
import requests
from bs4 import BeautifulSoup
import re

def scrape_and_save_to_csv(url, csv_filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract metadata
        metadata = soup.find('meta', attrs={'name': 'description'})
        metadata_content = metadata.get('content') if metadata else ''

        # Extract all links
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Extract all images
        images = [img['src'] for img in soup.find_all('img', src=True)]

        # Extract articles
        articles = []
        for article in soup.find_all('article'):
            title = article.find('h1', class_='title_inner').get_text().strip()
            one_liner = article.find('div',class_='use_case') .get_text().strip()
            tag = article.find('div', class_='tags').get_text().strip()
            website = article.find('div', class_='visit_website').get_text().strip()
           

        # Open CSV file for writing
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write header row
            writer.writerow(['Metadata', 'Links', 'Images', 'Title', 'one_liner', 'tag', 'website'])

            # Write data to CSV file
            writer.writerow([metadata_content, ', '.join(links), ', '.join(images), *[', '.join(row) for row in articles]])

        print(f"Data scraped successfully and saved to '{csv_filename}'")
    else:
        print('Failed to retrieve webpage:', response.status_code)

url = 'https://theresanaiforthat.com/'
csv_filename = 'theresanaiforthat_data2.csv'
scrape_and_save_to_csv(url, csv_filename)
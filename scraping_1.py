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
            title = article.find('h2', class_='entry-title').get_text().strip()
            date = article.find('time', class_='entry-date').get('datetime')
            author = article.find('span', class_='author vcard').get_text().strip()
            content = article.find('div', class_='entry-content').get_text().strip()
            articles.append([title, date, author, content])

        # Open CSV file for writing
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write header row
            writer.writerow(['Metadata', 'Links', 'Images', 'Title', 'Date', 'Author', 'Content'])

            # Write data to CSV file
            writer.writerow([metadata_content, ', '.join(links), ', '.join(images), *[', '.join(row) for row in articles]])

        print(f"Data scraped successfully and saved to '{csv_filename}'")
    else:
        print('Failed to retrieve webpage:', response.status_code)

url = 'https://theresanaiforthat.com/'
csv_filename = 'theresanaiforthat_data1.csv'
scrape_and_save_to_csv(url, csv_filename)
import requests
from bs4 import BeautifulSoup
import os
import time

def scrape_all_data(url, output_dir):
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    visited = set()  # Set to keep track of visited URLs
    stack = [url]    # Stack for DFS traversal

    # Create a session object with custom headers
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    session.headers.update(headers)

    while stack:
        current_url = stack.pop()

        # Skip if URL is already visited
        if current_url in visited:
            continue

        try:
            # Sending a GET request to the URL
            print(f"Requesting {current_url}...")
            response = session.get(current_url)

            # Checking if the request was successful (status code 200)
            if response.status_code == 200:
                # Parsing the HTML content of the page
                soup = BeautifulSoup(response.content, "html.parser")

                # Scraping text content
                text_content = soup.get_text()

                # Save text content to file
                text_filename = os.path.join(output_dir, f"{current_url.replace('/', '_')}_text.txt")
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)

                print(f"Text scraping completed for {current_url}. Text data saved to {text_filename}")

                # Scraping image URLs
                img_urls = [img['src'] for img in soup.find_all('img', src=True)]
                img_filename = os.path.join(output_dir, f"{current_url.replace('/', '_')}_images.txt")
                with open(img_filename, 'w', encoding='utf-8') as f:
                    for img_url in img_urls:
                        f.write(img_url + '\n')

                print(f"Image scraping completed for {current_url}. Image URLs saved to {img_filename}")

                # Scraping hyperlinks
                link_urls = [link['href'] for link in soup.find_all('a', href=True)]
                link_filename = os.path.join(output_dir, f"{current_url.replace('/', '_')}_links.txt")
                with open(link_filename, 'w', encoding='utf-8') as f:
                    for link_url in link_urls:
                        f.write(link_url + '\n')

                print(f"Link scraping completed for {current_url}. Hyperlinks saved to {link_filename}")

                # Add links on current page to the stack for further traversal
                for link in link_urls:
                    if link.startswith('/'):
                        link = url + link
                    stack.append(link)

            else:
                print(f"Failed to retrieve {current_url}. Status code: {response.status_code}")

            # Introduce a delay to avoid overwhelming the server
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Mark current URL as visited
        visited.add(current_url)

if __name__ == "__main__":
    site_url = "https://theresanaiforthat.com"
    output_directory = "theresanaiforthat_data"
    scrape_all_data(site_url, output_directory)

(acess gemini api)
(sai uses the same logics )
(stimulate the the reality )
......
import requests
from bs4 import BeautifulSoup

def scrape_wikipedia_headings(url, output_filename="wiki_headings.txt"):
    """
    Fetches a Wikipedia page, extracts all headings, and saves them to a file.

    Args:
        url (str): The URL of the Wikipedia page to scrape.
        output_filename (str): The name of the file to save the headings.
    """
    try:
        # 1. Fetch the HTML content from the specified URL
        print(f"Fetching content from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for bad status codes (4xx or 5xx)

        # 2. Parse the HTML using BeautifulSoup
        print("Parsing HTML content...")
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Find all heading tags (h1, h2, h3)
        headings = soup.find_all(['h1', 'h2', 'h3'])
        
        if not headings:
            print("No headings found on the page.")
            return

        # 4. Process and save the headings
        print(f"Found {len(headings)} headings. Saving to '{output_filename}'...")
        with open(output_filename, 'w', encoding='utf-8') as f:
            for heading in headings:
                heading_text = heading.get_text().strip()
                line = f"{heading.name}: {heading_text}\n"
                f.write(line)
                print(f"  - {line.strip()}")

        print(f"\nSuccessfully scraped and saved headings to '{output_filename}'.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main execution ---
if __name__ == "__main__":
    wikipedia_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    scrape_wikipedia_headings(wikipedia_url)
import requests
import time

def fetch_html(link, index):
    """
    Fetches the HTML content of the provided link and saves it to a file.

    Args:
    link (str): The URL to fetch the content from.
    index (int): The index of the link, used for naming the output file.
    """
    try:
        # Send a GET request to the link
        response = requests.get(link.strip())  # Strip any extra spaces/newlines from the link
        
        # Save the HTML content to a file
        with open(f"data/game{index}.html", "w", encoding="utf-8") as file:
            file.write(response.text)
            
    except requests.exceptions.RequestException as e:
        # Handle any potential request errors
        print(f"Failed to retrieve {link}: {e}")

def process_links(filepath, start_index=0):
    """
    Processes the links from the given file, fetching HTML content for each.

    Args:
    filepath (str): The path to the file containing links to process.
    start_index (int): The index from which to start processing (default is 0).
    """
    with open(filepath, "r") as links_file:
        for index, link in enumerate(links_file):
            # Start processing from the given index
            if index >= start_index:
                if len(link.strip()) > 5:  # Ensure the link is not empty or too short
                    print(f"Processing link at index {index}: {link.strip()}")
                    fetch_html(link, index)  # Fetch and save the HTML content

def main():
    """
    Main function to process all links from a text file and fetch their HTML content.
    """
    process_links("Scraper/cleaned_links.txt", start_index=2799)  # Start processing from index 2799

if __name__ == '__main__':
    main()

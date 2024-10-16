from bs4 import BeautifulSoup
import os
import pandas as pd

# Function to extract data from the HTML content
def extract_game_data(html_doc, link):
    soup = BeautifulSoup(html_doc, 'html.parser')

    game_data = {}

    # Extract the game title
    game_data["title"] = soup.find('h1').get_text()

    # Add the link to the game
    game_data["link"] = link.strip()

    # Extract the image link
    img_tag = soup.find("img", class_="T75of QhHVZd") or soup.find("img", class_="T75of Q3MhI NXRaDe")
    game_data["img"] = img_tag.get("src") if img_tag else None

    # Extract tags
    tags = [tag.get_text() for tag in soup.select(".Uc6QCc .VfPpkd-dgl2Hf-ppHlrf-sM5MNb")]
    game_data["tags"] = ",".join(tags)

    # Extract downloads
    download_info = soup.find_all(class_="ClM7O")
    game_data["downloads"] = download_info[1].get_text() if len(download_info) > 1 and download_info[1].get_text() else download_info[0].get_text()

    # Extract rating
    game_data["rating"] = download_info[0].get_text() if "star" in download_info[0].get_text() else "0.0 star"

    # Extract reviews
    review_info = soup.find(class_="g1rdde")
    game_data["reviews"] = review_info.get_text() if review_info and "Downloads" not in review_info.get_text() else "0 reviews"

    # Extract description
    description_tag = soup.find(class_="bARER")
    game_data["description"] = description_tag.get_text(separator='\n').split("\n")[0] if description_tag else None

    # Extract last update information
    last_update_tag = soup.find(class_="xg1aie")
    game_data["last_update"] = last_update_tag.get_text() if last_update_tag else None

    return game_data

# Main function to process all the files
def process_game_data():
    game_files = os.listdir("data")
    game_links = open("scraper/Cleaned_links.txt").readlines()

    data = {
        "title": [], "downloads": [], "rating": [], "reviews": [], "tags": [], 
        "description": [], "last_update": [], "link": [], "img": []
    }

    # Loop over each game HTML file and extract data
    for idx, file_name in enumerate(game_files):
        with open(f"data/{file_name}", encoding="utf-8") as f:
            html_doc = f.read()
            game_data = extract_game_data(html_doc, game_links[idx])

            # Append extracted data to the respective lists
            for key in data:
                data[key].append(game_data.get(key))

        print(f"Processed game {idx + 1}/{len(game_files)}")

        # Limit to first 5 games for testing purposes
        if idx == 5:
            break

    # Save the data to CSV
    pd.DataFrame(data).to_csv("Play_Store_Games.csv", index=False)

# Run the main function
if __name__ == "__main__":
    process_game_data()

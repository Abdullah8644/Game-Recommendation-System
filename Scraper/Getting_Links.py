from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

def initialize_driver():
    """
    Initializes the Chrome WebDriver and maximizes the window.
    
    Returns:
    WebDriver: An instance of the Chrome WebDriver.
    """
    service = Service(executable_path="Scraper/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

def scroll_to_bottom(driver):
    """
    Scrolls to the bottom of the page to load more content dynamically.
    
    Args:
    driver (webdriver): The WebDriver instance controlling the browser.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")  # Get the current scroll height
    
    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load (adjust if needed)
        time.sleep(2)
        
        # Get the new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Check if the scroll height has not changed, indicating the end of the page
        if new_height == last_height:
            break
        
        # Update the last height to the new one and continue scrolling
        last_height = new_height

def get_all_hrefs(driver):
    """
    Retrieves all valid href links from the current page.
    
    Args:
    driver (webdriver): The WebDriver instance controlling the browser.
    
    Returns:
    list: A list of href links found on the page.
    """
    links = driver.find_elements(By.TAG_NAME, "a")  # Find all anchor elements
    hrefs = [link.get_attribute("href") for link in links if link.get_attribute("href")]  # Filter out valid hrefs
    return hrefs

def write_links(links, destination="links"):
    """
    Writes a list of links to a text file.
    
    Args:
    links (list): A list of links to write to the file.
    destination (str): The filename (without extension) where links will be saved. Defaults to "links".
    """
    with open(f"{destination}.txt", "a") as f:
        for link in links:
            f.write(f"{link}\n")  # Write each link on a new line

def search_game(driver, name):
    """
    Searches for a game by name in the Google Play Store.
    
    Args:
    driver (webdriver): The WebDriver instance controlling the browser.
    name (str): The name of the game to search for.
    """
    driver.get("https://play.google.com/store/games?hl=en")  # Navigate to the Play Store games section

    # Find and click on the search button
    search_button = driver.find_element(By.XPATH, '//*[@id="kO001e"]/header/nav/div/div[1]/button/i')
    search_button.click()

    # Enter the game name into the search bar and press Enter
    search_bar = driver.find_element(By.XPATH, '//*[@id="kO001e"]/header/nav/c-wiz/div/div/label/input')
    search_bar.send_keys(name.strip())  # Ensure no extra spaces from the file input
    search_bar.send_keys(Keys.ENTER)

def process_game(driver, name):
    """
    Searches for a game, scrolls through the page, collects links, and writes them to a file.
    
    Args:
    driver (webdriver): The WebDriver instance controlling the browser.
    name (str): The name of the game to process.
    """
    search_game(driver, name)  # Search for the game
    scroll_to_bottom(driver)   # Scroll to load all the content
    time.sleep(3)              # Wait for the page to fully load
    
    # Get all the href links from the page
    links = get_all_hrefs(driver)
    print(links)               # Optional: Print the links for debugging
    write_links(links)         # Save the links to a file

def process_all_games(driver, filepath):
    """
    Processes all game names from the provided file by searching, scrolling, and extracting links.
    
    Args:
    driver (webdriver): The WebDriver instance controlling the browser.
    filepath (str): The path to the file containing the game names.
    """
    with open(filepath, "r") as file:
        for name in file:
            process_game(driver, name)  # Process each game name

def main():
    """
    Main function that sets up the WebDriver and processes game searches.
    """
    driver = initialize_driver()  # Initialize WebDriver
    process_all_games(driver, "Scraper/games.txt")  # Process game names from file
    
    time.sleep(10)  # Optional: Wait before closing
    driver.quit()   # Close the browser

if __name__ == '__main__':
    main()

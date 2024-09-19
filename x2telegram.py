from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Define the path to your Chrome user data directory and the profile name
user_data_dir = '/path/to/your/chrome/user/data'
profile_dir = 'Profile 2'

# Define Chrome options with the user data directory and profile directory
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={user_data_dir}")
chrome_options.add_argument(f"profile-directory={profile_dir}")

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

# File to store the last sent tweet content
last_sent_file = 'telegram_last_sent_tweet.txt'

# Function to read the last sent tweet content from a file
def read_last_sent_tweet():
    if os.path.exists(last_sent_file):
        with open(last_sent_file, 'r', encoding='utf-8') as file:
            return file.read().strip()
    return None

# Function to write the latest tweet content to a file
def write_last_sent_tweet(content):
    with open(last_sent_file, 'w', encoding='utf-8') as file:
        file.write(content)

while True:
    try:
        # Open the X.com (formerly Twitter) profile page
        driver.get('https://x.com/ghazayel')

        # Wait for the page to load completely
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//article[1]//div[@lang]')))

        # Find the newest tweet on the page
        newest_tweet = driver.find_element(By.XPATH, '//article[1]//div[@lang]')

        # Extract the text content of the tweet
        tweet_content = newest_tweet.text
        print(f"Latest Tweet: {tweet_content}")

        # Check if the tweet content is the same as the last sent tweet
        last_sent_tweet = read_last_sent_tweet()
        if tweet_content == last_sent_tweet:
            print("Tweet already sent. Waiting for the next check...")
        else:
            # Open the Telegram channel
            driver.get('https://web.telegram.org/k/#@ghazayel')

            # Wait for the Telegram Web channel to load
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Broadcast"]')))

            # Find the message input box that is associated with the placeholder "Broadcast"
            input_box = driver.find_element(By.XPATH, '//span[text()="Broadcast"]/ancestor::div[contains(@class, "input-message-container")]/div[contains(@class, "input-message-input")]')
            
            # Clear any existing text (optional)
            input_box.clear()

            # Find the message input box within that context
            input_box.send_keys(tweet_content)

            # Simulate pressing Enter to send the message
            input_box.send_keys(Keys.RETURN)

            # Update the last sent tweet content in the file
            write_last_sent_tweet(tweet_content)

            print("Tweet sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Wait for 2 minutes before running the script again
    time.sleep(120)

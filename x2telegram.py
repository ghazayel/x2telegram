from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import os

# Specify the user data directory and profile directory (FIX USERNAME)
user_data_dir = r'C:\Users\USERNAME\AppData\Local\Microsoft\Edge\User Data'
profile_dir = 'Profile 1'

edge_options = Options()
edge_options.add_argument(f"user-data-dir={user_data_dir}")
edge_options.add_argument(f"profile-directory={profile_dir}")
# edge_options.add_argument("--disable-gpu")  # Disable GPU acceleration
# edge_options.add_argument("--headless")  # Run in headless mode (optional)
# edge_options.add_argument("--remote-debugging-port=9222")
# edge_options.add_argument("--no-sandbox")
# edge_options.add_argument("--disable-dev-shm-usage")


# Initialize the Edge WebDriver with options INSTALL DRIVER
driver = webdriver.Edge(service=Service('C:/edgedriver/msedgedriver.exe'), options=edge_options)

# File to store the last sent tweet content
last_sent_file = 'telegram_last_sent_tweet.txt'

# Function to read the last sent tweet content from a file
def read_last_sent_tweet():
    try:
        if os.path.exists(last_sent_file):
            with open(last_sent_file, 'r', encoding='utf-8') as file:
                return file.read().strip()
    except Exception as e:
        print(f"Error reading last sent tweet: {e}")
    return None

# Function to write the latest tweet content to a file
def write_last_sent_tweet(content):
    try:
        with open(last_sent_file, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing last sent tweet: {e}")

# Remove specific word from sentence
def remove_word(sentence, word_to_remove):
    updated_sentence = sentence.replace(word_to_remove, '')
    return ' '.join(updated_sentence.split())

while True:
    try:
        # Open the X.com (formerly Twitter) profile page of ghazayel
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
            sentence = tweet_content
            word_to_remove = ['عاجل |', 'عاجل|']

            for word in word_to_remove:
                if word in sentence:
                    new_tweet_content = remove_word(sentence, word)
                    break
            else:
                new_tweet_content = sentence

            new_tweet_content = new_tweet_content.replace('_', ' ').replace('#', '')

            # Open the Telegram channel
            driver.get('https://web.telegram.org/k/#@ghazayel')

            # Wait for the Telegram Web channel to load
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Broadcast"]')))
            
            # Try to find the message input box associated with the placeholder "Broadcast"
            try:
                input_box = driver.find_element(By.XPATH, '//span[text()="Broadcast"]/ancestor::div[contains(@class, "input-message-container")]/div[contains(@class, "input-message-input")]')
            except NoSuchElementException:
                # Handle the case where "Broadcast" is not found
                print("Broadcast element not found. Trying to find the input box without it.")
                input_box = driver.find_element(By.XPATH, '//div[contains(@class, "input-message-container")]/div[contains(@class, "input-message-input")]')

            # Clear any existing text (optional)
            input_box.clear()

            # Send the new tweet content
            # input_box.send_keys(new_tweet_content)
            # input_box.send_keys(Keys.RETURN)
           
            # new code here
            driver.execute_script("arguments[0].innerText = arguments[1];", input_box, new_tweet_content)
            input_box.send_keys(Keys.ENTER)


            # Update the last sent tweet content in the file
            write_last_sent_tweet(tweet_content)

            print("Tweet sent successfully!")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Element not found or timed out: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pass
    
    # Wait for 2 minutes before running the script again
    time.sleep(120)

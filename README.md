# Telegram Bot for Sending Tweets from Twitter (X.com) using Microsoft Edge

This project is a Python automation script that fetches the latest tweet from a Twitter (X.com) profile and sends it to a specified Telegram channel using **Selenium WebDriver**. The script is designed to work with **Microsoft Edge** and automates the process of sending content from X.com to Telegram.

## Features

- Automates Microsoft Edge using Selenium to fetch the latest tweet from a Twitter profile.
- Strips specific unwanted words (e.g., `عاجل |`) from the tweet.
- Sends the tweet to a Telegram channel using **Telegram Web**.
- Ensures no duplicate tweets are sent by tracking the last sent tweet.
- Automatically retries every 2 minutes to fetch new tweets.

## Requirements

- Python 3.x
- Microsoft Edge and [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- Selenium (`pip install selenium`)

## Setup

1. **Install the required Python libraries:**
    ```bash
    pip install selenium
    ```

2. **Download Edge WebDriver:**
    - Make sure you have Microsoft Edge installed.
    - Download the [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) corresponding to your Edge version.
    - Place it in a directory, e.g., `C:/edgedriver/msedgedriver.exe`.

3. **Modify the script:**
    - Update the `user_data_dir` and `profile_dir` paths in the script to match your Edge user profile. You can find the user data directory in the Edge settings under `Profile`.
    - Change the `driver.get()` URLs to point to the correct X.com profile and Telegram channel.

    ```python
    user_data_dir = r'C:\Users\YOUR_USERNAME\AppData\Local\Microsoft\Edge\User Data'
    profile_dir = 'Profile 1'
    ```

4. **Run the script:**
    - Execute the script with Python:
    ```bash
    python script.py
    ```

## Script Workflow

1. **Initialization:**
    - The script launches Microsoft Edge with your specified profile to maintain login sessions for X.com and Telegram Web.
    
2. **Fetch Tweet:**
    - The script navigates to the X.com profile of 20fourMedia (`https://x.com/20fourLive`).
    - It scrapes the latest tweet's text content and removes unwanted words such as `عاجل |`.

3. **Send to Telegram:**
    - The script navigates to your Telegram channel (`https://web.telegram.org/k/#@live20four`).
    - It locates the input box, clears it, and sends the tweet content using the Telegram Web interface.
    
4. **Check for Duplicates:**
    - The script checks the latest tweet against the last sent tweet stored in `telegram_last_sent_tweet.txt` to avoid sending duplicates.

5. **Retry Mechanism:**
    - The script runs in an infinite loop, checking for new tweets every 2 minutes.

## Customization

- **Headless Mode:** To run the browser without a visible window, uncomment the following line in the script:
    ```python
    edge_options.add_argument("--headless")
    ```

- **Error Handling:** The script includes basic error handling for elements not found or page load timeouts. Adjust the waiting times as necessary.

## Example Output

The script prints the latest tweet's content and logs successful Telegram posts in the terminal.

```bash
Latest Tweet: Breaking news...
Tweet sent successfully!

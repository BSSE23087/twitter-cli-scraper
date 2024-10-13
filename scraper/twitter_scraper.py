import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import argparse

# Set up the driver using webdriver-manager
def setup_driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

# Scrape trending topics from Twitter
def get_trends(username, password):
    driver = setup_driver()
    driver.get("https://twitter.com/login")
    time.sleep(5)

    # Log in to Twitter
    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(username)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(5)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    driver.find_element(By.XPATH, "//span[text()='Log in']").click()
    time.sleep(10)

    driver.get("https://twitter.com/i/trends")
    time.sleep(5)

    trends = []
    keywords = []
    articles = driver.find_elements(By.XPATH, "//div[@data-testid='trend']")
    
    for article in articles:
        try:
            keyword = article.find_element(By.XPATH, ".//div[@class='css-1rynq56']").text
            trending = article.find_element(By.XPATH, ".//span[contains(text(),'Trending')]").text
        except NoSuchElementException:
            keyword = article.find_element(By.XPATH, ".//span[@class='css-1qaijid']").text
            trending = article.find_element(By.XPATH, ".//span[contains(text(),'Trending')]").text
        
        trends.append(trending)
        keywords.append(keyword)

    df = pd.DataFrame(zip(trends, keywords), columns=['Trending', 'Keyword'])
    df.to_excel("trends.xlsx", index=False)
    print("Trends scraped successfully!")
    
    driver.quit()

# Scrape tweets for a specific trend
def scrape_tweets(username, password, trend, fields):
    driver = setup_driver()
    driver.get("https://twitter.com/login")
    time.sleep(5)

    # Log in to Twitter
    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(username)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(5)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    driver.find_element(By.XPATH, "//span[text()='Log in']").click()
    time.sleep(10)

    # Search for the trend
    search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
    search_box.send_keys(trend)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    # Scraping logic
    tweets_data = []
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

    for article in articles:
        tweet_info = {}
        tweet_info['User'] = article.find_element(By.XPATH, "//div[@data-testid='User-Name']").text
        tweet_info['Timestamp'] = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
        tweet_info['Tweet'] = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

        if 'images' in fields:
            try:
                image = article.find_element(By.XPATH, "//div[@data-testid='tweetPhoto']//img")
                tweet_info['Image'] = image.get_attribute("src")
            except NoSuchElementException:
                tweet_info['Image'] = None

        if 'likes' in fields:
            tweet_info['Likes'] = article.find_element(By.XPATH, ".//div[@data-testid='like']").text

        tweets_data.append(tweet_info)

    df = pd.DataFrame(tweets_data)
    df.to_excel("tweets.xlsx", index=False)
    print(f"Tweets for {trend} scraped successfully!")

    driver.quit()

# Main CLI entry point
def main():
    parser = argparse.ArgumentParser(description="Twitter Scraper Tool")
    parser.add_argument("--username", type=str, required=True, help="Twitter username")
    parser.add_argument("--password", type=str, required=True, help="Twitter password")
    parser.add_argument("--action", type=str, choices=["scrape_trends", "scrape_tweets"], required=True,
                        help="Action to perform: scrape trends or scrape tweets.")
    parser.add_argument("--trend", type=str, help="Trend name for scraping tweets (required if action is scrape_tweets)")
    parser.add_argument("--fields", type=str, nargs='*', default=["tweets"], help="Fields to scrape: e.g., tweets, images, likes")

    args = parser.parse_args()

    if args.action == "scrape_trends":
        get_trends(args.username, args.password)
    elif args.action == "scrape_tweets":
        if not args.trend:
            parser.error("scrape_tweets action requires --trend")
        scrape_tweets(args.username, args.password, args.trend, args.fields)

if __name__ == "__main__":
    main()

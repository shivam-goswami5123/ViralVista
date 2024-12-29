import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import uuid
import time
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
MONGO_URI = os.getenv("MONGO_URI")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
PROXY = os.getenv("PROXY")


# Get the public IP address used for requests
try:
    #With Proxy
    response = requests.get("https://httpbin.org/ip",proxies={"http": PROXY, "https": PROXY})
    #Without Proxy
    # response = requests.get("https://httpbin.org/ip")
    proxy_ip = response.json().get("origin", "Unknown")
except Exception as e:
    print(f"Error fetching IP: {e}")
    proxy_ip = "Unknown"




# MongoDB Setup
client = MongoClient(MONGO_URI)
db = client['test']  # Database name
collection = db['trends']  # Collection name


#Set up Selenium with proxy

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://%s' % PROXY)

driver = webdriver.Chrome(options=chrome_options)


#Set up Selenium without proxy
# chrome_options = webdriver.ChromeOptions()

# driver = webdriver.Chrome(options=chrome_options)

try:
    # Step 1: Open Twitter Login Page
    driver.get("https://x.com/login")

    # Increase the timeout duration to 20 seconds
    username = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    username.send_keys(TWITTER_USERNAME)
    username.send_keys(Keys.RETURN)

    # Wait for the password input field
    password = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password.send_keys(TWITTER_PASSWORD)
    password.send_keys(Keys.RETURN)

    # Step 2: Wait for the home page to load completely
    # Wait until a specific element that indicates the page has fully loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='primaryColumn']"))
    )

    # Now the home page is loaded, proceed to the next page
    driver.get("https://x.com/explore/tabs/for-you")
    time.sleep(5)

    # Step 3: Save the complete HTML page to trends.html
    page_source = driver.page_source
    with open("trends.html", "w", encoding="utf-8") as file:
        file.write(page_source)

    print("HTML page saved as trends.html")

    # Step 4: Parse trends.html to extract the top 6 trends
    with open("trends.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Locate all divs with data-testid="cellInnerDiv"
    all_divs = soup.find_all("div", {"data-testid": "cellInnerDiv"})
    trends = []

    # List of required classes for the inner div
    required_classes = [
        "css-146c3p1", "r-bcqeeo", "r-1ttztb7", "r-qvutc0", 
        "r-37j5jr", "r-a023e6", "r-rjixqe", "r-b88u0q", "r-1bymd8e"
    ]

    
    for div in all_divs[1:6]: 
        # Find the inner div that matches all the required classes
        inner_div = div.find("div", class_=lambda class_name: all(cls in class_name for cls in required_classes))

        if inner_div:
            # Now find the span with class 'css-1jxf684' inside the inner div
            span = inner_div.find("span", class_="css-1jxf684")
            if span and span.text:
                trends.append(span.text)

    # print("Top Trends:", trends)

    # Step 5: Save trends to MongoDB
    if trends:
        data = {
            "uniqueID": str(uuid.uuid4()),
            "trend1": trends[0] if len(trends) > 0 else None,
            "trend2": trends[1] if len(trends) > 1 else None,
            "trend3": trends[2] if len(trends) > 2 else None,
            "trend4": trends[3] if len(trends) > 3 else None,
            "trend5": trends[4] if len(trends) > 4 else None,
            "timestamp": datetime.now(),
            "ipAddress": proxy_ip,  # Since no proxy is used
        }
        collection.insert_one(data)
        print("Trends saved to MongoDB")
    else:
        print("No trends found")

finally:
    driver.quit()

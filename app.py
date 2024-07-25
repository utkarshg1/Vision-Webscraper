import os
from dotenv import load_dotenv
import random

# Load dotenv
load_dotenv()
host = os.getenv("HOST")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
session_id = random.random()
proxy_url = f"wss://{username}:{password}@{host}"

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={proxy_url}")
chrome = webdriver.Chrome(options=chrome_options)
chrome.get("https://www.google.com")

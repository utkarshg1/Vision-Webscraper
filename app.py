from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import base64
import requests
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables
load_dotenv()

def get_screenshot(url):
    # Setup headless chrome
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # define a function to get scroll dimensions
    def get_scroll_dimension(axis):
        return driver.execute_script(f"return document.body.parentNode.scroll{axis}")
    
    driver.get(url)
    print(driver.title)

    # get the page scroll dimensions
    width = get_scroll_dimension("Width")
    height = get_scroll_dimension("Height")

    # set the browser window size
    driver.set_window_size(width, height)

    # get the full body element
    full_body_element = driver.find_element(By.TAG_NAME, "body")

    # take a full-page screenshot
    full_body_element.screenshot("screenshot.png")

    # quit the browser
    driver.quit()

    # Print file saved
    print("File saved as screenshot.png")

def image_to_base64(image_path="screenshot.png"):
    """
    Encode an image to base64.
    
    Args:
    image_path (str): The path to the image file.
    
    Returns:
    str: The base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def get_model_response(encoded_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": ("You will get screenshot of a webpage"
                            "Based on screenshot Please scrape the data"
                            "and provide results in json format only")
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            }
            ]
        }
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    completion = response.json()
    return completion["choices"][0]["message"]["content"]

if __name__ == "__main__":
    st.set_page_config(
        page_title="Vision Scraper - Utkarsh",
        page_icon="👁️",
        layout="wide"
    )
    st.title("Vision WebScraper 🤖 - Utkarsh Gaikwad")
    url = st.text_input("Please enter url you want to scrape : ")
    if url:
        with st.spinner("scraping..."):
            get_screenshot(url)
            encoded_image = image_to_base64()
            st.subheader("Model Response : ")
            completion = get_model_response(encoded_image)
            st.write(completion)
        
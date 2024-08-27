import os
import re
import json
import time
import requests
from datetime import datetime

import numpy as np
import pandas as pd

from tqdm import tqdm
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from src.general_utils import util

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Send a GET request to the website
def parse_url(driver, url: str, timeout: int = 10):
    if driver is None:
        driver = webdriver.Firefox()

    else:
        # Define a function to open links in new tabs
        driver.execute_script("window.open('');")

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
    try:
        # Set the page load timeout
        driver.set_page_load_timeout(timeout)

        # Open the URL
        # print(f"Loading page: {url}")
        driver.get(url)
    except TimeoutException:
        print(
            f"Page load exceeded {timeout} seconds. Continuing with scraping...")

    # Try to close the popup if it appears
    try:
        # Locate the close button for the popup and click it
        popup_close_button = driver.find_element(
            By.CSS_SELECTOR, 'button.mfp-close')
        popup_close_button.click()
        time.sleep(2)  # Wait a moment for the popup to close

    except Exception as e:
        print("Popup not found or unable to close it:", e)

    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, 'html.parser')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return driver, soup


url_list = [
    # "https://www.wickedweasel.com/en-us/outerwear/skirts",
    # 'https://www.wickedweasel.com/en-us/outerwear/top',
    # 'https://www.wickedweasel.com/en-us/outerwear/pants',
    # 'https://www.wickedweasel.com/en-us/outerwear/loungewear',
    # 'https://www.wickedweasel.com/en-us/outerwear/jumpsuit',
    'https://www.wickedweasel.com/en-us/outerwear/shorts',
    'https://www.wickedweasel.com/en-us/outerwear/dress',


    # 'https://www.wickedweasel.com/en-us/activewear/legging',
    # 'https://www.wickedweasel.com/en-us/activewear/packs',
    # 'https://www.wickedweasel.com/en-us/activewear/swimwear',

    # 'https://www.wickedweasel.com/en-us/lingerie/bralette',
    # 'https://www.wickedweasel.com/en-us/lingerie/cami-bra',
    # 'https://www.wickedweasel.com/en-us/lingerie/crop-bra',
    # 'https://www.wickedweasel.com/en-us/lingerie/slip',
    # 'https://www.wickedweasel.com/en-us/lingerie/panties',
    # 'https://www.wickedweasel.com/en-us/lingerie/thong',
    # 'https://www.wickedweasel.com/en-us/lingerie/micro-thong',
    # 'https://www.wickedweasel.com/en-us/lingerie/bodysuit',
    # 'https://www.wickedweasel.com/en-us/lingerie/knicker-pack',
    # 'https://www.wickedweasel.com/en-us/lingerie/sleepwear',

    # 'https://www.wickedweasel.com/en-us/bikinis/lined',
    # 'https://www.wickedweasel.com/en-us/bikinis/one-piece-bikini',
    # 'https://www.wickedweasel.com/en-us/bikinis/crop-bikini-top',
    # 'https://www.wickedweasel.com/en-us/bikinis/halter-top-bikini',
    # 'https://www.wickedweasel.com/en-us/bikinis/bandeau-bikini-top',
    # 'https://www.wickedweasel.com/en-us/bikinis/underwire-bikini-top',
    # 'https://www.wickedweasel.com/en-us/bikinis/tri-top-bikini'
]

base_product_url = 'https://www.wickedweasel.com'
driver = None

for url in url_list:
    # print(f'URL: {url}')
    # URL to scrape
    url_basename = os.path.basename(url)
    url_type = url.split('/')[-2]

    path_output_dir = f'/Users/manish.sahu/Downloads/tiler/scrap-bookmyshow/data/wickedweasel/images/{url_type}/{url_basename}'

    util.check_dir(path_output_dir)

    # Create a new driver and parse the URL
    if driver:
        driver.quit()
        driver = None

    driver, soup = parse_url(driver=driver, url=url)

    # Find all the dress containers (adjust selectors based on the website's structure)
    dress_containers = soup.find_all('div', class_='product-tile')

    # Extract details for each dress
    for dress in tqdm(dress_containers):
        try:
            product_name = dress.text.strip().replace(' ', '-')

            if product_name == 'promo':
                continue

            product_url = base_product_url + \
                dress.find(class_='product-item')['href']

            # print(f'product_url: {product_url}')
            path_image_dir = os.path.join(path_output_dir, product_name)
            util.check_dir(path_image_dir)

            _, product_soup = parse_url(
                driver=driver, url=product_url, timeout=5)

            image_list = product_soup.find_all(
                class_='carousel-container')[0].find_all('li')
            number_of_images = len(image_list)

            for i in range(number_of_images):
                image_url = image_list[i].find('img')['src']
                basename = os.path.basename(image_url).split('?')[0]
                path_image = os.path.join(path_image_dir, f'{basename}')

                if not os.path.exists(path_image):
                    response = requests.get(image_url)
                    with open(path_image, 'wb') as f:
                        f.write(response.content)
                    # print(f"Downloaded: {path_image}")
                else:
                    # print(f"Already exists: {path_image}")
                    pass
        except Exception as e:
            print(f"Error: {e}")
            continue

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
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class GetMovieDetails:
    def __init__(self, path_movie_url, movie_name, date, location, 
                 if_debug=False):

        self.path_movie_url = path_movie_url
        self.movie_name = movie_name
        self.date = date
        self.location = location
        self.formatted_time = self._get_current_time()
        self.if_debug = if_debug

    def _get_current_time(self):
        # Get the current time in seconds since the epoch
        current_time_seconds = time.time()

        # Convert seconds since the epoch to a time structure
        time_struct = time.localtime(current_time_seconds)

        # Format the time in 24-hour format (HH:MM:SS)
        formatted_time = time.strftime("%H:%M", time_struct)
        return formatted_time

    def _get_header(self):
        headers = {
            'Referer': 'https://in.bookmyshow.com/explore/movies-bengaluru?languages=hindi',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Linux",
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        return headers

    def _get_fake_user_agent(self):
        options = Options()
        options.add_argument("window-size=1400,600")
        ua = UserAgent()
        user_agent = ua['google chrome']
        
        options.add_argument(f'user-agent={user_agent}')
        return options
    
    def _get_chrome_driver(self):
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        options = self._get_fake_user_agent()
                
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome()
        driver.get(self.path_movie_url)
        return driver

    def convert_to_json(self, data_categories: str):
        return json.loads(data_categories)

    def get_price(self, data_json):
        return data_json.get('price')

    def get_desc(self, data_json):
        return data_json.get('desc')

    def get_availability_class(self, data_json):
        return data_json.get('availabilityClass')

    def get_availStatus(self, data_json):
        return data_json.get('availStatus')

    def get_processed_df(self):
        driver = self._get_chrome_driver()

        if self.if_debug:
            print(driver)
        theatre_element_list = driver.find_elements(By.CLASS_NAME, 'list')
        if self.if_debug:
            print(f'Number of theatres : {len(theatre_element_list)}')

        data = []

        for i, a in enumerate(theatre_element_list):
            try:
                titles = a.find_element(By.CLASS_NAME, '__title')
                listing_info = a.find_elements(By.CLASS_NAME, 'listing-info')
                showtimes = a.find_elements(By.CLASS_NAME, 'showtime-pill')

                for s in showtimes:

                    data_categories = self.convert_to_json(
                        s.get_attribute('data-categories'))
                    timings = s.get_attribute('data-date-time')

                    temp_data = {
                        'cinema_title': titles.text.split('\nINFO')[0],
                        'timings': timings,
                        'latitude': a.get_attribute('data-lat'),
                        'longtitude': a.get_attribute('data-lng'),

                        'price': self.get_price(data_categories),
                        'description': self.get_desc(data_categories),

                        'availability_class': self.get_availability_class(data_categories),
                        'avail_status': self.get_availStatus(data_categories),
                        'movie_name': self.movie_name,
                        'date': self.date,
                        'location': self.location,
                        'checked_time': self.formatted_time,
                    }

                    data.append(temp_data)

                # b.find_element('showtime-pill')
            except Exception as e:
                if self.if_debug:
                    print(i)

        data_df = pd.DataFrame(data)

        return data_df

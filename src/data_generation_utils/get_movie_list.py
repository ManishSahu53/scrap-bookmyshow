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

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class GetMoviesList:
    def __init__(self, path_movie_list_url, location, date):
        self.date = date
        self.location = location
        self.path_movie_list_url = path_movie_list_url
        self.movie_ahref_string = f'https://in.bookmyshow.com/{location}/movies'

    def _get_header(self):
        headers = {
            'Referer': 'https://in.bookmyshow.com/explore/movies-bengaluru?languages=hindi',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Linux",
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        return headers

    def _get_chrome_driver(self):
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        driver = webdriver.Chrome()
        driver.get(self.path_movie_list_url)

        # Scroll to buttom slowly to load all movies
        driver.execute_async_script(
            """
        count = 400;
        let callback = arguments[arguments.length - 1];
        t = setTimeout(function scrolldown(){
            console.log(count, t);
            window.scrollTo(0, count);
            if(count < (document.body.scrollHeight || document.documentElement.scrollHeight)){
              count+= 400;
              t = setTimeout(scrolldown, 1000);
            }else{
              callback((document.body.scrollHeight || document.documentElement.scrollHeight));
            }
        }, 1000);"""
        )
        return driver

    def parse_drive_to_soup(self, driver):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup

    def get_all_current_movie_list(self, soup):

        movie_soup_element_dict = {}

        movie_tags_list = [a for a in soup.find_all(
            'a', href=True) if self.movie_ahref_string in a['href']]

        # Extract movie names from the URLs
        movie_names = []
        for link in movie_tags_list:
            # Extract the movie name from the URL
            movie_name_match = re.search(r'.*/movies/(.*)/ET.*', link['href'])
            if movie_name_match:
                movie_name = movie_name_match.group(1)
                movie_names.append(movie_name)

                movie_url = link['href']
                movie_url_basename = movie_url.split('/')[-1]

                movie_booking_url = f'https://in.bookmyshow.com/buytickets/{movie_name}-{self.location}/movie-bang-{movie_url_basename}-MT/{self.date}'

                movie_soup_element_dict[movie_name] = {
                    # 'element': link,
                    'url': movie_url,
                    'name': movie_name,
                    'booking_url': movie_booking_url,
                    'date': self.date,
                    'location': self.location,
                }

        # # Print the movie names
        # for movie_name in movie_names:
        #     print("Movie Name:", movie_name)

        print(f'Number of movies running: {len(movie_names)}')
        return movie_soup_element_dict

    def generate(self):
        driver = self._get_chrome_driver()
        soup = self.parse_drive_to_soup(driver)
        movie_soup_element_dict = self.get_all_current_movie_list(soup)

        return movie_soup_element_dict

import os
import re

import time
from datetime import datetime

import pandas as pd

from tqdm import tqdm
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.general_utils import util
from src.data_generation_utils.get_movie_list import GetMoviesList
from src.data_generation_utils.get_movie_details import GetMovieDetails

from config import params

config = params.MovieConfig()

for location in config.location_list:
    print(f'Processing location: {location}')
    # location = 'national-capital-region-ncr'
    # Get the current date
    current_date = datetime.now()
    # Format the date in YYYYMMDD format
    date = current_date.strftime("%Y%m%d")
    # Get the current time in seconds since the epoch
    current_time_seconds = time.time()

    # Convert seconds since the epoch to a time structure
    time_struct = time.localtime(current_time_seconds)

    # Format the time in 24-hour format (HH:MM:SS)
    formatted_time = time.strftime("%H:%M", time_struct)

    path_movie_list_url = f'https://in.bookmyshow.com/explore/movies-{location}'
    path_output_dir = 'data/'

    #######################
    path_output_data_csv = os.path.join(
        path_output_dir, f'{location}/{date}/data_{location}_{date}.csv')
    path_output_data_json = os.path.join(
        path_output_dir, f'{location}/{date}/data_{location}_{date}.json')

    print(f'path_output_data_csv: {path_output_data_csv}')

    #######################
    movie_list_instance = GetMoviesList(
        path_movie_list_url=path_movie_list_url, location=location, date=date)
    movie_soup_element_dict = movie_list_instance.generate()

    util.check_dir(os.path.dirname(path_output_data_json))
    util.save_json(movie_soup_element_dict, path_output=path_output_data_json)

    #######################
    data_movie_list = []

    for movie_name in tqdm(movie_soup_element_dict):
        path_movie_url = movie_soup_element_dict[movie_name]['booking_url']

        movie_details = GetMovieDetails(path_movie_url=path_movie_url,
                                        location=location, date=date,
                                        movie_name=movie_name,

                                        )
        movie_detail_df = movie_details.get_processed_df()
        data_movie_list.append(movie_detail_df)

    data_movie_list_pd = pd.concat(data_movie_list)

    if os.path.exists(path_output_data_csv):
        data_movie_list_pd.to_csv(
            path_output_data_csv, index=False, mode='a', header=False)
    else:
        data_movie_list_pd.to_csv(
            path_output_data_csv, index=False, mode='a', header=True)

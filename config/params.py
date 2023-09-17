from dataclasses import field
from dataclasses import dataclass
from typing import List


@dataclass
class MovieConfig:
    """Class for keeping track of an item in inventory."""

    path_data_dir = '/Users/manish.sahu/Downloads/tiler/scrap-bookmyshow/data/'
    location_list = [
        'bhopal',
        'bengaluru',
        'national-capital-region-ncr',
        'mumbai',
        'chennai',
        'kolkata',
        'indore',
        'chandigarh',
        'ahmedabad',
        'hyderabad',
        'pune',
        'kochi',
        'varanasi',
        'jaipur',
        'bhubaneswar',
    ]

    mapping_available_status = {
        0: 'sold',
        1: 'low_availablity',
        2: 'medium_available',
        3: 'high_available',
    }

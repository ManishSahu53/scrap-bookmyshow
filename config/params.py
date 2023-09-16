from dataclasses import dataclass

@dataclass
class MovieConfig:
    """Class for keeping track of an item in inventory."""
    
    path_data_dir: str = '/Users/manish.sahu/Downloads/tiler/scrap-bookmyshow/data/'
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
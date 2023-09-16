import os
import pandas as pd
from datetime import datetime

from src.general_utils import util

class MovieDataLoder:
    def __init__(self, path_data_dir):
        self.path_data_dir = path_data_dir
        self.city_list = self._get_folder_list(path_data_dir)
        self.city_date_mapping = {city: self._get_folder_list(os.path.join(path_data_dir, city)) for city in self.city_list}
        self.city_date_csv_mapping = self._get_city_date_csv_dict_mapping()
            
    def get_date_data(self, data_df, date):
        temp_df = data_df[data_df['date'] == date]
        return temp_df
    
    def get_city_data(self, city):
        date_list = self.city_date_csv_mapping.get(city)
        
        data_city_df = []
        for date in date_list:
            csv_list = date_list.get(date)
            for csv in csv_list:
                df = self._read_csv(csv)
                data_city_df.append(df)
                
        data_city_df = pd.concat(data_city_df)
        data_city_df['date'] = data_city_df['date'].apply(lambda x: str(x))
        
        data_city_df['movie_time_std'] = data_city_df['timings'].apply(lambda x: datetime.strptime(x, '%I:%M %p'))
        data_city_df['checked_time_std'] = data_city_df['checked_time'].apply(lambda x: datetime.strptime(x, '%H:%M'))

        data_city_df['difference'] = data_city_df.apply(lambda x: (x['movie_time_std'] - x['checked_time_std']).seconds//3600, axis=1)
        data_city_df['Date'] = data_city_df.date.apply(lambda x: datetime.strptime(x, '%Y%m%d').date())

        del data_city_df['movie_time_std']
        del data_city_df['checked_time_std']
        
        return data_city_df
    
    def get_label_list(self, data_city_df, label_column):
        movie_list = list(data_city_df.groupby(['movie_name', 'cinema_title']).count().reset_index().sort_values('timings', ascending=False)['movie_name'].unique())
        return movie_list

    def get_movie_screen_count(self, city_df):
        city_df_dedup = city_df.drop_duplicates(subset=['movie_name', 'cinema_title', 'timings', 'Date'])
        
        data_df = city_df_dedup.groupby(['movie_name', 'Date']).count().reset_index()[['movie_name', 'cinema_title', 'Date']]
        
        data_df = data_df.rename(columns={'cinema_title': 'Number of Shows', 'movie_name': 'Movies'})
        data_df['Movies'] = data_df['Movies'].apply(lambda x: str(x).upper())
        
        # data_df['Date'] = data_df.date.apply(lambda x: datetime.strptime(x, '%Y%m%d').date())
        
        data_df = data_df.sort_values('Number of Shows', ascending=False)
        return data_df
    
    
    def get_mean_tick_price(self, city_df):
        data_df = city_df.groupby(['movie_name', 'Date']).mean('price').reset_index()[['movie_name', 'price', 'Date']]
            
        data_df['price'] = data_df['price'].apply(lambda x: (x//10)*10)
        
        data_df = data_df.rename(columns={'price': 'Mean Ticket Price', 'movie_name': 'Movies',})
        data_df['Movies'] = data_df['Movies'].apply(lambda x: str(x).upper())
        # data_df['Date'] = data_df.date.apply(lambda x: datetime.strptime(x, '%Y%m%d').date())

        return data_df

        
    def get_number_of_shows(self, data_city_df):
        n = len(data_city_df.drop_duplicates(subset=['movie_name', 'cinema_title', 'timings']))
        return n

    
    def _get_folder_list(self, path_data_dir):
        return os.listdir(path=path_data_dir)    
        
    def _read_csv(self, path_csv):
        return pd.read_csv(path_csv)
    
    def _get_city_date_csv_dict_mapping(self):
        city_date_csv_dict = {}
        for city in self.city_list:
            city_date_csv_dict[city] = {}
            for date in self.city_date_mapping[city]:
                path_csv_list = util.list_list(os.path.join(self.path_data_dir, city, date), '.csv')
                city_date_csv_dict[city][date] = path_csv_list
                
        return city_date_csv_dict
    
    
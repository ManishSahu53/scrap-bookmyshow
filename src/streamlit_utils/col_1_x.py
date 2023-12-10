import pandas as pd
import streamlit as st
import plotly.express as px

from src.data_utils.data_loader import MovieDataLoder


class Column_1_X_Loader:
    def __init__(self, movie_data_loader: MovieDataLoder, date):
        self.movie_data_loader = movie_data_loader

    def get_col_1_1(self, col_1_1, city_list):
        movie_city = col_1_1.selectbox('Select City', city_list, )
        return movie_city

    def get_col_1_2(self, col_1_2, movie_city, date):
        city_df = self.movie_data_loader.get_city_data(movie_city)
        
        date_city_df = self.movie_data_loader.get_date_data(data_df=city_df, date=date)
        
        cinema_title_list = self.movie_data_loader.get_label_list(
            date_city_df, label_column='cinema_title')
        
        movie_list = self.movie_data_loader.get_label_list(
            date_city_df, label_column='movie_name')

        total_shows = self.movie_data_loader.get_number_of_shows(date_city_df)
        
        # col_1_2.markdown(f"<plaintext style='text-align; center;'> Number of Cinema Halls </plaintext>",  unsafe_allow_html=True)
        col_1_2.text('Number of Cinema Halls')
        col_1_2.markdown(
            f"<h3 style='text-align: left; color: blue'>{len(cinema_title_list)}</h2>", unsafe_allow_html=True)

        # col_1_2.markdown(f"<plaintext style='text-align; center;'> Number of Movies </plaintext>",  unsafe_allow_html=True)
        col_1_2.text('Number of Movies')
        col_1_2.markdown(
            f"<h3 style='text-align: left; color: blue'>{len(movie_list)}</h2>", unsafe_allow_html=True)


        # col_1_2.markdown(f"<plaintext style='text-align; center;'> Number of Movies </plaintext>",  unsafe_allow_html=True)
        col_1_2.text('Total Number of Shows')
        col_1_2.markdown(
            f"<h3 style='text-align: left; color: blue'>{total_shows}</h2>", unsafe_allow_html=True)
        
        return cinema_title_list, movie_list

    def get_col_1_3(self, col_1_3, movie_city, date):
        city_df = self.movie_data_loader.get_city_data(movie_city)
        
        date_city_df = self.movie_data_loader.get_date_data(data_df=city_df, date=date)
        
        data_movie_screen = self.movie_data_loader.get_movie_screen_count(
            city_df=date_city_df)
                
        data_movie_price = self.movie_data_loader.get_mean_tick_price(
            city_df=date_city_df)

        data_movie_screen_price = pd.merge(
            data_movie_screen, data_movie_price, on='Movies', how='inner')

        fig = px.bar(data_movie_screen_price,
                     x='Movies', y='Number of Shows',
                    #  color_discrete_sequence=['rgb(255, 140, 0)']
        )
        
        # Add the line chart and update its color to red
        line_chart_trace = px.line(data_movie_screen_price, x="Movies", y="Mean Ticket Price")\
                             .update_traces(
                                yaxis="y2",
                                line=dict(color='red', shape='spline'),
                                mode='lines+markers')\
                             .data

        line_chart_trace[0]['line']['color'] = 'red'

        fig.add_traces(line_chart_trace)
        fig.update_layout(
            yaxis2={"side": "right", "overlaying": "y", "color": "red"})
        fig.update_layout(
            # Turn off grid lines for the primary y-axis
            yaxis={"showgrid": True},
            # Turn off grid lines for the secondary y-axis
            yaxis2={"showgrid": False}
        )

        col_1_3.plotly_chart(fig, use_container_width=True)
        return city_df

import pandas as pd
import streamlit as st
import plotly.express as px

from src.data_utils.data_loader import MovieDataLoder


class Column_2_X_Loader:
    def __init__(self, movie_data_loader: MovieDataLoder, date):
        self.movie_data_loader = movie_data_loader
        self.date = date
        self.mapping_avail_status = {
            0: 'Sold Out',
            1: 'Low Availablity',
            2: 'Medium Availablity',
            3: 'High Availablity',
        }
        self.color_mapping = {'Sold Out': '#cc3333', 'Low Availablity': '#ff9999',
                              'Medium Availablity': '#80d4ff', 'High Availablity': '#47d147'}

        self.custom_status_order = ['High Availablity',
                                    'Medium Availablity', 'Low Availablity',
                                    'Sold Out']
        self.category_orders = {"status": self.custom_status_order}

    def get_col_2_2(self, col_2_2, movie_city, movie_name):

        # Movie - Price - Shows Times series
        city_df = self.movie_data_loader.get_city_data(movie_city)
        movie_city_df = city_df[city_df['movie_name'] == movie_name]

        data_movie_screen = self.movie_data_loader.get_movie_screen_count(
            city_df=movie_city_df)

        data_movie_price = self.movie_data_loader.get_mean_tick_price(
            city_df=movie_city_df)

        data_movie_screen_price = pd.merge(
            data_movie_screen, data_movie_price, on=['Movies', 'Date'], how='inner')

        fig = px.bar(data_movie_screen_price,
                     x='Date', y='Number of Shows',
                     title='Number of Shows Available Timeline',
                     #  color_discrete_sequence=['rgb(255, 140, 0)']
                     )

        # Add the line chart and update its color to red
        line_chart_trace = px.line(data_movie_screen_price, x="Date", y="Mean Ticket Price")\
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

        col_2_2.plotly_chart(fig, use_container_width=True)
        return movie_city_df

    def get_col_2_3(self, col_2_3, movie_city, movie_name):

        city_df = self.movie_data_loader.get_city_data(movie_city)
        movie_city_df = city_df[city_df['movie_name'] == movie_name]

        movie_df_one_hour = movie_city_df[movie_city_df['difference'] == 0]
        movie_df_one_hour['status'] = movie_df_one_hour['avail_status'].apply(
            lambda x: self.mapping_avail_status.get(x))
        movie_df_one_hour['count'] = 1

        movie_df_one_hour_percentage = movie_df_one_hour.groupby(
            ['status', 'Date']).agg({'count': 'sum'}).reset_index()
        total_cinema_df = movie_df_one_hour.groupby(
            ['Date']).agg({'count': 'sum'}).reset_index()
        total_cinema_df = total_cinema_df.rename(
            columns={'count': 'total_cinema_count'})

        movie_df_one_hour_percentage = pd.merge(
            movie_df_one_hour_percentage, total_cinema_df, on='Date', how='left')
        movie_df_one_hour_percentage['percentage'] = movie_df_one_hour_percentage.apply(
            lambda x: x['count']*100//x['total_cinema_count'], axis=1)

        fig = px.bar(movie_df_one_hour_percentage, x='Date', y='percentage',
                     color='status',
                     color_discrete_map=self.color_mapping,
                     title='% Availability 1 Hour Before of Show Time',
                     labels={'Date': 'Date', 'percentage': 'Percentage'},
                     barmode='group',
                     category_orders={"status": self.custom_status_order}
                     )  # Set barmode to 'group' for side-by-side bars

        col_2_3.plotly_chart(fig, use_container_width=True)

        return movie_df_one_hour_percentage

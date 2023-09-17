# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import os
import logging
import traceback
from datetime import datetime

from config import params

from src.general_utils import util
from src.data_utils import data_loader
from src.streamlit_utils import col_1_x, col_2_x

import numpy as np
import pandas as pd

import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='Pardex - Movie power analysis',
                   page_icon=":chart_with_upwards_trend:",
                   layout='wide', initial_sidebar_state='collapsed')

st.title('Pardex', )


LINE = """<style>
.vl {
  border-left: 2px solid black;
  height: 100px;
  position: absolute;
  left: 50%;
  margin-left: -3px;
  top: 0;
}
</style>
<div class="vl"></div>"""

config = params.MovieConfig()
# Format the date in YYYYMMDD format
current_date = str(datetime.now().strftime("%Y%m%d"))

movie_data_loader = data_loader.MovieDataLoder(config.path_data_dir)
movie_index = 0
movie_city = movie_data_loader.city_list[movie_index]

try:
    date_index = movie_data_loader.city_date_mapping[movie_city].index(current_date)
except:
    date_index = 0

movie_date = movie_data_loader.city_date_mapping[movie_city][date_index]

# Row 1
col_1_1, col_1_2, col_1_3, col_1_4 = st.columns([2, 2, 8, 1, ])


col_1_x_loader = col_1_x.Column_1_X_Loader(movie_data_loader=movie_data_loader,
                                           date=movie_date)

col_2_x_loader = col_2_x.Column_2_X_Loader(movie_data_loader=movie_data_loader,
                                           date=movie_date)

# Row 1 Column 1 - Cities
movie_city = col_1_x_loader.get_col_1_1(col_1_1, movie_data_loader.city_list)

# Row 1 Column 1 - Cinema List
cinema_title_list, movie_list = col_1_x_loader.get_col_1_2(col_1_1, movie_city, date=movie_date)

# Row 1 Column 2 - Movie Dates
movie_date = col_1_2.selectbox('Select Date', movie_data_loader.city_date_mapping[movie_city],
                               index=date_index)

# Row 1 Column 3
movie_screen_df = col_1_x_loader.get_col_1_3(col_1_3, movie_city, date=movie_date)

# col_1_1

st.title('Movie Analysis', )
col_2_1, col_2_2, col_2_3, col_2_4 = st.columns([3, 8, 8, 1, ])
movie_name = col_2_1.selectbox('Select Movie', movie_list, movie_index)

movie_city_df = col_2_x_loader.get_col_2_2(col_2_2,
                                           movie_city=movie_city,
                                           movie_name=movie_name)

movie_status_percentage = col_2_x_loader.get_col_2_3(col_2_3,
                                                     movie_city=movie_city,
                                                     movie_name=movie_name)

# query_params = st.experimental_get_query_params()

# col3.write("**[Linkedin](https://www.linkedin.com/in/manishsahuiitbhu/)<br>[:beer:]**",
#            unsafe_allow_html=True)
# options = ['Infection', 'Vaccines']

# what = col1.radio('Type of Data', options)
# area = col2.selectbox("Region", list(config.POPULATION_MAP.keys()))

# if what == 'Infection':
#     st.header('Real time data updated till {}'.format(
#         current_date.strftime('%Y-%m-%d')))

#     col1, line, col3, col4, col5, col6, col7, col8 = st.columns(
#         [10, 1, 8, 8, 8, 8, 8, 8])
#     line.markdown(LINE, unsafe_allow_html=True)

#     with col1:
#         rule = st.radio('', list(config.RULE_MAP.keys()))
#         st.write('')
#         log = st.checkbox('Log Scale', False)

#     # Daily Confirmed Cases
#     with col3:
#         st.markdown("<h3 style='text-align: center;'>Daily Cases</h2>",
#                     unsafe_allow_html=True)

#         if area.lower() == 'india':
#             try:
#                 value = daily_overall['Daily Confirmed'].values[0]
#             except Exception as e:
#                 logging.error(
#                     f'Error: {e}. Cannot get data for overall India, Date: {current_date}')
#                 value = 0

#         else:
#             try:
#                 value = data_state['daily_confirmed'].values[0]
#             except Exception as e:
#                 logging.error(
#                     f'Error: {e}. Cannot get data for State level wise, Date: {current_date}')
#                 value = 0

#         temp_confirmed = custom_plot.normalisation(
#             value, config.POPULATION_MAP[area], rule)
#         text = f'{temp_confirmed:.2f}' if config.RULE_MAP[
#             rule] == 'percentage' else f'{int(temp_confirmed):,}'

#         st.markdown(
#             f"<h2 style='text-align: center; color: red;'>{text}</h1>", unsafe_allow_html=True)


#     if area == 'India':
#         graph_data = data_time_series
#         graph_positive_data = data_positivity_overall
#     else:
#         graph_data = data_state_cls.data[data_state_cls.data['State'] == area]
#         graph_positive_data = data_state_cls.data

#     coln, _, _, _, _, _, _ = st.columns([8, 4, 8, 8, 8, 8, 8])
#     type_of_timeseries = coln.selectbox(
#         "", ['Daily Cases', 'Daily Recoveries', 'Daily Deaths', 'Daily Tests', 'Positivity Rate'])

#     x = graph_data['date'][-365:].values

#     if type_of_timeseries == 'Daily Cases':
#         type_of_timeseries = 'Number of Confirmed Cases'
#         y = graph_data['daily_confirmed'][-365:].values

#     elif type_of_timeseries == 'Daily Recoveries':
#         type_of_timeseries = 'Number of Recoveries'
#         y = graph_data['daily_recovered'][-365:].values

#     elif type_of_timeseries == 'Daily Deaths':
#         type_of_timeseries = 'Number of Deaths'
#         y = graph_data['daily_deceased'][-365:].values

#     elif type_of_timeseries == 'Daily Tests':
#         type_of_timeseries = 'Number of Tests (Moving Average 7)'
#         x = data_tested_overall_cls.data['date'][-365:].values
#         y = data_tested_overall_cls.data['daily_test'].rolling(
#             7).mean()[-365:].values

#     elif type_of_timeseries == 'Positivity Rate':
#         x = graph_positive_data['date'][-365:].values
#         y = graph_positive_data['positivity_rate'][-365:].rolling(
#             7).mean()[-365:].values


#     if log:
#         y = np.log(y)

#     fig2 = px.line(y=y,
#                    x=x,
#                    title='Daily Statistics',
#                    labels={'y': type_of_timeseries,
#                            'x': 'Time Period'},
#                    line_shape='spline',
#                    )

#     fig2.add_vline(x='2020-09-16',
#                    line_width=1,
#                    line_dash="dash",
#                    line_color="Orange")

#     fig2.add_vline(x='2021-02-18',
#                    line_width=1,
#                    line_dash="dash",
#                    line_color="Red")

#     fig2.add_hline(y=5,
#                   line_width=1,
#                   line_dash="dash",
#                   line_color="Green",
#                   annotation_text="Required Positivity Rate",
#                   annotation_position="bottom left",
#                   )

#     fig2.update_layout(legend=dict(
#         orientation="h",
#         yanchor="bottom",
#         y=1.02,
#         xanchor="right",
#         x=1
#     ),
#         xaxis_fixedrange=True,
#         yaxis_fixedrange=True,
#         dragmode=False,
#         plot_bgcolor="white"
#     )

#     st.plotly_chart(fig2, use_container_width=True)

#     ########################### Second Chart #################################
#     fig = px.area(y=100*graph_data['percent_growth_active_case'].rolling(7).mean()[-365:].values,
#                   x=graph_data['date'][-365:].values,
#                   title='Overall India Growth Rate of Active Cases (7 Day Moving Average)',
#                   labels={'y': '% Growth Active Case',
#                           'x': 'Time Period'},
#                   line_shape='spline',
#                   )

#     fig.add_hline(y=0,
#                   line_width=1,
#                   line_dash="dash",
#                   line_color="Green",
#                   annotation_text="Recovery > Cases",
#                   annotation_position="bottom left",
#                   )

#     fig.add_vline(x='2020-09-16',
#                   line_width=1,
#                   line_dash="dash",
#                   line_color="Orange")

#     fig.add_vline(x='2021-02-18',
#                   line_width=1,
#                   line_dash="dash",
#                   line_color="Red")

#     fig.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)'),
#                       xaxis_fixedrange=True,
#                       yaxis_fixedrange=True,
#                       dragmode=False,
#                       plot_bgcolor="white",)
#     st.plotly_chart(fig, use_container_width=True)

#     ########################### Third Chart #################################
#     rule = st.selectbox('Variables', [
#                         'Daily Recovery', 'Daily New Cases', 'Daily Deaths', 'Daily Test', 'Daily Active Cases'])
#     st.plotly_chart(custom_plot.summary(
#         data_state_cls.data, rule), use_container_width=True)

# elif what == 'Vaccines':
#     # Loading Vaccine Dataset
#     data_vaccine_cls = data_loader.DataVaccineState(
#         config.path_vaccine_state_wise_cowin)
#     data_vaccine_cls.process()

#     st.header('Real time data updated till {}'.format(
#         current_date.strftime('%Y-%m-%d')))

#     # Loading Full india or State wise
#     data_vaccine = data_vaccine_cls.data[(data_vaccine_cls.data['State'] == area) & (
#         data_vaccine_cls.data['date'] <= current_date)]

#     pie1, title1, line, pie2, title2, title3, title4 = st.columns([
#                                                                        2, 4, 1, 2, 4, 4, 4])
#     line.markdown(LINE, unsafe_allow_html=True)

#     # Total Individuals Vaccinated
#     with pie1:
#         total_population = config.POPULATION_MAP[area]
#         vaccine_population = data_vaccine['Total Individuals Vaccinated'].values[-1]
#         labels = ['Population Vaccinated',  'Populaton not Vaccinated']
#         x = vaccine_population
#         y = total_population - vaccine_population

#         st.plotly_chart(custom_plot.plot_population(
#             [x, y], labels, area, height=180, t=0), use_container_width=True)

#     # Total Individuals Vaccinated
#     with title1:
#         st.markdown("<h3 style='text-align: center;'>Total Person Vaccinated</h2>",
#                     unsafe_allow_html=True)

#         value = int(data_vaccine['Total Individuals Vaccinated'].values[-1])
#         st.markdown(
#             f"<h1 style='text-align: center; color: red;'>{value:,}</h1>", unsafe_allow_html=True)

#     # Type of Vaccines Administered
#     with pie2:
#         x = data_vaccine[' Covaxin (Doses Administered)'].values[-1]
#         y = data_vaccine['CoviShield (Doses Administered)'].values[-1]
#         labels = ['Covaxin Vaccine',  'CovidShield Vaccine']
#         st.plotly_chart(custom_plot.plot_population(
#             [x, y], labels, area, height=180, t=0), use_container_width=True)


#     # Time Series dataset
#     x = data_vaccine['date'][-90:]
#     y = [data_vaccine['daily_first'].values[-90:],
#          data_vaccine['daily_second'].values[-90:]]
#     names = ['First Dose', 'Second Dose']
#     title = 'Total Vaccinated'
#     st.plotly_chart(custom_plot.plot_bar(x=x, y=y, name=names,
#                                          title=title), use_container_width=True)

#     col1, col2 = st.columns(2)

#     # daily_covaxin', 'daily_covidshield
#     with col1:
#         x = data_vaccine['date'][-90:]
#         y = [data_vaccine['daily_covaxin'].values[-90:],
#              data_vaccine['daily_covidshield'].values[-90:]]
#         names = ['Covaxin', 'CovidShield']

#         title = 'Type of Vaccines'
#         st.plotly_chart(custom_plot.plot_bar(
#             x=x, y=y, name=names, title=title), use_container_width=True)


#     pie1, pie2, pie3 = st.columns(1)

#     # Age wise Distribution
#     with pie1:
#         st.markdown("<h3 style='text-align: center;'>Age wise Distribution</h2>",
#                     unsafe_allow_html=True)
#         labels = ['18-45 years', '45-60 years', '60+ years']
#         values = [
#             data_vaccine['18-44 Years (Doses Administered)'].values[-1],
#             # data_vaccine['30-45 years (Age)'].values[-1],
#             data_vaccine['45-60 Years (Doses Administered)'].values[-1],
#             data_vaccine['60+ Years (Doses Administered)'].values[-1]
#         ]

#         pie1.plotly_chart(custom_plot.plot_population(
#             values, labels, area, legend=True, height=200, t=0), use_container_width=True)


# else:
#     st.header(f'Please select from options: {options}')

# st.write("**:beer: Buy me a s[beer]**")
# expander = st.expander("This app is developed by Manish Sahu.")
# expander.write(
#     "Contact me on [Linkedin](https://www.linkedin.com/in/manishsahuiitbhu/)")
# expander.write(
#     "The source code is on [GitHub](https://github.com/ManishSahu53/streamlit-covid-dashboard)")

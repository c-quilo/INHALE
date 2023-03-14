import streamlit as st
import numpy as np
#import pyvista as pv
import pandas as pd
import streamlit as st
import pydeck as pdk
import ssl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

from observation_display import obsdisplay
from data_assimilation import dataAssimilation
from slice2pandas import vtu2pandas
from slice2pandas import vtu2pandasAll
from mapDisplay import scatterMap
from mapDisplay import columnMap

st.set_page_config(
    page_title = 'Inhale',
    page_icon = '🫁🌳',
    initial_sidebar_state = 'expanded',
    layout = 'wide',
)
c1, c2, c3, c4, c5 = st.columns([0.8, 1, 1, 1, 1])
c1.image('./logos/INHALE.png', use_column_width=True)
c2.image('./logos/ICL.png')
c3.image('./logos/Surrey.png')
c4.image('./logos/UoE.png')
c5.image('./logos/UKRI.png')
st.write(
    """<style>
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

with st.sidebar:
    input_form = st.form(key='input_form')

    input_form.selectbox('Choose pollutant', ['PM1', 'PM2.5', 'PM10'])
    input_form.selectbox('Choose observation dates', ['August 2020', 'March 2021', 'October 2022'])

    c1, c2, c3 = input_form.columns((1, 1, 1))
    calculate_button = c1.form_submit_button('Calculate')
    c3.form_submit_button('Reset')

########Output Form
    output_form = st.form(key='output_form')
    output_form.header("Map data")
    # get rid of ssl connection error (certificates)
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


    # read in data`

    df = pd.read_csv(r'pointLocations.csv', sep=',')
    r = scatterMap(df)
    output_form.pydeck_chart(r)

    # output of clicked point should be input to a reusable list
    selectedID = output_form.selectbox("Choose Location", df['Location']) 
    display_button = output_form.form_submit_button('Display')
    display_all_button = output_form.form_submit_button('Display all')
    
##### Main layout

m1, m2 = st.columns(2)

if display_button:
    midpoint = (df.loc[df['Location'] == selectedID])
    mid_lat = np.average(midpoint['Latitude'])
    mid_lon = np.average(midpoint['Longitude'])
    zoom_level = 14

    #data = vtu2pandas(mid_lat, mid_lon, 1)
    #data.to_csv(f'./points_interest_{selectedID}_1.csv')
    data_1m = pd.read_csv(f'./csv/points_interest_{selectedID}_1.csv')

    r1 = columnMap(data_1m, mid_lat, mid_lon, zoom_level)
    m1.pydeck_chart(r1)

    #data = vtu2pandas(mid_lat, mid_lon, 1.7)
    #data.to_csv(f'./points_interest_{selectedID}_1.7.csv')
    data_17m = pd.read_csv(f'./csv/points_interest_{selectedID}_1.7.csv')

    r2 = columnMap(data_17m, mid_lat, mid_lon, zoom_level)
    m2.pydeck_chart(r2)

    pm_values = pd.concat([data_1m['Values'], data_17m['Values']], axis=1)
    pm_values = pm_values.set_axis(['Children', 'Adults'], axis=1, inplace=False)
    st.line_chart(pm_values)

if display_all_button:
    mid_lat, mid_lon = (np.average(df["Latitude"]), np.average(df["Longitude"]))
    zoom_level = 14

    #data = vtu2pandasAll(df, height=1)
    data_1m = pd.read_csv('./csv/points_interest_all_1.csv')
    r3 = columnMap(data_1m, mid_lat, mid_lon, zoom_level)
    m1.pydeck_chart(r3)

    #data = vtu2pandasAll(df, height=1.7)
    data_17m = pd.read_csv('./csv/points_interest_all_1.7.csv')
    r4 = columnMap(data_17m, mid_lat, mid_lon, zoom_level)
    m2.pydeck_chart(r4)

    pm_values = pd.concat([data_1m['Values'], data_17m['Values']], axis=1)
    pm_values = pm_values.set_axis(['Children', 'Adults'], axis=1, inplace=False)
    st.line_chart(pm_values)

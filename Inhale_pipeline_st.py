import streamlit as st
import numpy as np
import pyvista as pv
from stpyvista import stpyvista
import gmaps
import pandas as pd
from ipywidgets import embed
import streamlit.components.v1 as components
import vtktools
from observation_display import obsdisplay
from data_assimilation import dataAssimilation

st.set_page_config(
    page_title = 'Inhale',
    page_icon = '🫁🌳',
    initial_sidebar_state = 'expanded',
    layout = 'wide',
)

st.title('Inhale')
st.subheader('Health assessment across biological length scales for personal pollution exposure and its mitigation')

input_form = st.form(key='vtuform')

c1, c2, c3 = st.columns(3)

c1.radio('Choose observation date1', ['August 2020', 'March 2021', 'October 2022'])
with c2:    
    c2.radio('Choose observation date2', ['August 2020', 'March 2021', 'October 2022'])
c3.radio('Choose observation date3', ['August 2020', 'March 2021', 'October 2022'])
c1.radio('Choose observation date4', ['August 2020', 'March 2021', 'October 2022'])

import streamlit as st
import pydeck as pdk
import pandas as pd
import ssl

# get rid of ssl connection error (certificates)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

st.header("Map data")
# read in data`
df = pd.read_csv(r'pointLocations.csv', sep=',')

layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    filled=True,
    radius_scale=5,
    radius_min_pixels=10,
    radius_max_pixels=500,
    line_width_min_pixels=0.01,
    get_position='[Longitude, Latitude]',
    get_fill_color=[255, 0, 0],
    get_line_color=[0, 0, 0],
)

# Set the viewport location
view_state = pdk.ViewState(latitude=df['Latitude'].iloc[-1], longitude=df['Longitude'].iloc[-1], zoom=14, min_zoom= 10, max_zoom=30)

# Render
r = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/satellite-v9',
                initial_view_state=view_state, tooltip={"html": "<b>Location: </b> {Location} <br /> "
                                                                "<b>Longitude: </b> {Longitude} <br /> "
                                                                "<b>Latitude: </b>{Latitude} <br /> "
                                                                })
r

# output of clicked point should be input to a reusable list
selectedID = st.selectbox("Choose Location", df['Location']) 


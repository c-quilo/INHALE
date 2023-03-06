import streamlit as st
import numpy as np
import pyvista as pv
from stpyvista import stpyvista
from observation_display import obsdisplay

st.set_page_config(
    page_title = 'Inhale',
    page_icon = '🫁🌳',
    initial_sidebar_state = 'expanded',
)
st.title('Inhale')
st.subheader('Health assessment across biological length scales for personal pollution exposure and its mitigation')
#Load file implementation
#@st.cache_data

uploaded_vtu = st.file_uploader('Upload .vtu file')
vtuform = st.form(key='vtuform')
vtu_button = vtuform.form_submit_button('Visualise .vtu')
if uploaded_vtu:
    mesh = pv.read(uploaded_vtu.name)
    #Load the mesh from the uploaded .vtu file
    scalarName = 'allSources'
    mesh.set_active_scalars('sensorField')
if vtu_button:
        st.write('South Kensington, London, UK')
        plotter = pv.Plotter(window_size=[600,600])

        #Add mesh to the plotter
        cmap = 'jet'
        single_slice = mesh.slice(normal=[0, 0, 1], origin=[0, 0, 1])
        plotter.add_mesh(single_slice, cmap=cmap, clim = [0, 50])
        # Camera
        plotter.camera_position = 'xy'
        plotter.camera.zoom(2)

        stpyvista(plotter, key='South Kensington')


#Load .csv and visualise

#Visualise observed data
i = 20
obsform = st.form(key='obsdata')

uploaded_csv = obsform.file_uploader('Upload .csv data file', accept_multiple_files=True)
filenameCollection = []
if uploaded_csv:
   for uploaded_file in uploaded_csv:
       filenameCollection.append(uploaded_file.name)

#Slider to choose radius

radius = obsform.slider(
    'Select a radius of influence',
    0.0, 20.0, (5.0))

st.write('Radius:', radius)
sensorField = obsdisplay(filenameCollection, mesh, radius, i)
zeroField = 0*mesh[scalarName]
mesh['sensorField'] = zeroField
mesh['sensorField'] = sensorField

obs_button = obsform.form_submit_button('Visualise Observations')

if obs_button:

    mesh.set_active_scalars('sensorField')
    single_slice = mesh.slice(normal=[0, 0, 1], origin = [0, 0, 0.01])
    cmap = 'jet'
    p = pv.Plotter(window_size=[600,600])
    p.add_mesh(single_slice, cmap=cmap, clim = [0, 50])
    #Camera
    p.camera_position = 'xy'
    p.camera.zoom(1.4)
    stpyvista(p, key='Observational data')

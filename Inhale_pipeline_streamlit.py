import streamlit as st
import numpy as np
import pyvista as pv
import stpyvista as stpv

st.set_page_config(
    page_title = 'Inhale',
    page_icon = '🫁🌳',
    initial_sidebar_state = 'expanded',
)


#Load file implementation
#@st.cache_data

# uploaded_vtu = st.file_uploader('Upload .vtu file')
# if uploaded_vtu is not None:
#     @st.cache_data
#     def vtu_file_loader():
#         uploaded_file = uploaded_vtu
#         return uploaded_file

# uploaded_file = vtu_file_loader()

# st.title('South Kensington, London, UK')
# plotter = pv.Plotter(window_size=[400,400])

# #Load the mesh from the uploaded .vtu file
# mesh = pv.read(uploaded_file)
# scalarName = 'nut'
# #Add mesh to the plotter
# plotter.add_mesh(mesh, scalars=scalarName, cmap='jet', line_width=1)

# plotter.view_isometric()
# plotter.background_color = 'white'

# stpv(plotter, key='South Kensington')

# ipythreejs does not support scalar bars :(
pv.global_theme.show_scalar_bar = False 

## Initialize a plotter object
plotter = pv.Plotter(window_size=[400,400])

## Create a mesh with a cube 
mesh = pv.Cube(center=(0,0,0))

## Add some scalar field associated to the mesh
mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]

## Add mesh to the plotter
plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)

## Final touches
plotter.view_isometric()

## Pass a key to avoid re-rendering at each time something changes in the page
stpv(plotter, key="pv_cube")
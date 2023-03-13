import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

def scatterMap(df):
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
        get_fill_color=[255, 20, 0],
        get_line_color=[0, 0, 0],
    )

    # Set the viewport location
    midpoint = (np.average(df["Latitude"]), np.average(df["Longitude"]))
    view_state = pdk.ViewState(latitude=midpoint[0], longitude=midpoint[1], zoom=14, min_zoom= 10, max_zoom=30)

    # Render
    r = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/satellite-v9',
                        initial_view_state=view_state, tooltip={"html": "<b>Location: </b> {Location} <br /> "
                                                                        "<b>Longitude: </b> {Longitude} <br /> "
                                                                        "<b>Latitude: </b>{Latitude} <br /> "
                                                                        })
    return r

def columnMap(df, mid_lat, mid_lon, zoom_level):
    plasma = cm = plt.get_cmap('jet') 
    cNorm  = colors.Normalize(vmin=df["Values"].min(), vmax=df["Values"].max())
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=plasma)
    df["color"] = df.apply (lambda row: scalarMap.to_rgba(row["Values"]), axis=1)

    layer = pdk.Layer(
    "ColumnLayer",
    df,
    get_position=['Longitude', 'Latitude'],
    auto_highlight=True,
    get_elevation='Values',
    elevation_scale=1,
    radius=0.5,
    pickable=True,
    get_fill_color = "[color[0] * 255, color[1] * 255, color[2] * 255, color[3] * 255]",
    coverage=1
    )

    # Set the viewport location

    view_state = pdk.ViewState(latitude=mid_lat, longitude=mid_lon, zoom=zoom_level, min_zoom= 10, max_zoom=30, pitch=50)

    # Render
    r = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/light-v11',
                        initial_view_state=view_state)
    
    return r
 
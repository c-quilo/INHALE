import pandas as pd
import pyvista as pv
import pyproj
import numpy as np

import pyvista as pv
import numpy as np
import pyproj

def vtu2pandas(newlat, newlon, height):
    mesh = pv.read('/Users/cequilod/SK_1.vtu')
    slice = mesh.slice(normal=[0, 0, 1], origin=[0, 0, height])
    outProj = pyproj.Proj(init='EPSG:4326')
    inProj = pyproj.Proj(init='EPSG:27700')
    lon, lat = np.array(pyproj.transform(inProj, outProj, slice.points[:, 0], slice.points[:, 1]))
    df = pd.DataFrame()
    df['Longitude'] = lon
    df['Latitude'] = lat
    df['Values'] = slice['PS_PCAE_allTracers']

    north = newlat + 0.0001
    south = newlat - 0.0001
    east = newlon + 0.0001
    west = newlon - 0.0001

    df = df[(df['Latitude'] <= north) & (df['Latitude'] >= south)]
    df = df[(df['Longitude'] <= east) & (df['Longitude'] >= west)]
    df = df.reset_index()
    return df

def vtu2pandasAll(df, height):
    mesh = pv.read('/Users/cequilod/SK_1.vtu')
    slice = mesh.slice(normal=[0, 0, 1], origin=[0, 0, height])
    outProj = pyproj.Proj(init='EPSG:4326')
    inProj = pyproj.Proj(init='EPSG:27700')
    lon, lat = np.array(pyproj.transform(inProj, outProj, slice.points[:, 0], slice.points[:, 1]))

    df_collect = pd.DataFrame()
    for index, row in df.iterrows():
        newlat = row['Latitude']
        newlon = row['Longitude']
            
        temp = pd.DataFrame()
        temp['Longitude'] = lon
        temp['Latitude'] = lat
        temp['Values'] = slice['PS_PCAE_allTracers']

        north = newlat + 0.0001
        south = newlat - 0.0001
        east = newlon + 0.0001
        west = newlon - 0.0001

        temp = temp[(temp['Latitude'] <= north) & (temp['Latitude'] >= south)]
        temp = temp[(temp['Longitude'] <= east) & (temp['Longitude'] >= west)]
        df_collect = df_collect.append(temp, ignore_index=True)
    df_collect.to_pickle(f'./points_interest_all_{height}.pkl')
    return df_collect


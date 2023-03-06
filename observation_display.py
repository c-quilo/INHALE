import pandas as pd
import pyproj
from pyproj import Proj, transform
from scipy.spatial import cKDTree
import random
import numpy as np
import pyvista as pv

#directory = '/Users/cequilod/SouthKensington/'
def obsdisplay(filenames, mesh, r, i):
    year = 2020
    month = 8
    day = 10
    hour_start = 13
    minute_start = i
    second_start = 0
    hour_end = 14
    minute_end = i + 5
    second_end = 0

    if i == 55:
        minute_end = 0
        hour_end = 14

    kd_tree = cKDTree(mesh.points)
    nNeighbours = 1000
    radius = r

    #Projection to mesh's coordinates from WGS1984
    inProj = Proj(init='EPSG:4326')
    outProj = Proj(init='EPSG:27700')
    k = 0
    for filenameSensor in filenames:
        df = pd.read_csv('./' + filenameSensor)
        df['timestamp'] = pd.to_datetime(df['timestamp'], format = '%Y%m%d %H:%M:%S')

        #elif k == 5:
        #    year = 2021
        #    month = 3
        #    day = 2
        dfTemp = df[(df['timestamp'] > pd.Timestamp(year, month, day, hour_start, minute_start, second_start))
                    & (df['timestamp'] < pd.Timestamp(year, month, day, hour_end, minute_end, second_end))]
        locationSensor = np.zeros((int(dfTemp.index.shape[0]), 2))
        locationSensor[:, 0] = np.array(dfTemp['gpsLongitude'])
        locationSensor[:, 1] = np.array(dfTemp['gpsLatitude'])
        if k == 0:
            locationSensor[:, 0] = -0.178918
            locationSensor[:, 1] = 51.49559784
        elif k == 1:
            locationSensor[:, 0] = -0.16389534
            locationSensor[:, 1] = 51.48537064
        elif k == 2:
            locationSensor[:, 0] = -0.17486483
            locationSensor[:, 1] = 51.50166321
        elif k == 3:
            locationSensor[:, 0] = -0.18027534
            locationSensor[:, 1] = 51.50132751

        sensorPm2_5 = dfTemp['pm2_5']
        for j in range(dfTemp.index.shape[0]):
            projSensor = np.array(pyproj.transform(inProj, outProj, locationSensor[j, 0], locationSensor[j, 1]))
            pairs = kd_tree.query([projSensor[0], projSensor[1], 0.1], k=nNeighbours)
            nPointsRadius = np.where(pairs[0] <= radius)[0].shape[0]
            weightsTemp = 1/pairs[0][np.nonzero(pairs[0][:nPointsRadius])]
            weights = (weightsTemp/np.sum(weightsTemp))
            #print(np.sum(weights))

            #mesh['sensorField'][pairs[1][0][0:nPointsRadius]] = 90000
            mesh['sensorField'][pairs[1][np.nonzero(pairs[0][:nPointsRadius])]] = sensorPm2_5.iloc[j]*weights*weights.shape[0]
        k = k+1

 

    #ug = vtktools.vtu(filename)
    sensorField = mesh['sensorField']
    return sensorField
    #Create 104 zeroed fields and project the GPS of the mobile airspeck sensor
    # Interpolation of the GPS sensor to the nearest node
    #meshOriginal = mesh.copy()

    #from scipy.spatial import cKDTree
    #import random
    #mesh['LineSources'][np.where(np.isnan(mesh['LineSources']))] = 0
    #kd_tree = cKDTree(mesh.points)
    #nNeighbours = 1000
    #radius = 10
    #pointsFloor = np.array(np.where(mesh['LineSources'] > 1))
    #from time import sleep
    #from tqdm import tqdm



    #for i in progressbar(range(pointsFloor.shape[1]), 'Computing: ', 100):
    #    np.random.seed(42)
        #randomIndex = random.randint(0, pointsFloor.shape[1])
        #pairs = kd_tree.query(mesh.points[pointsFloor[0][i]], k=nNeighbours)
        #nPointsRadius = np.where(pairs[0][0] <= radius)[0].shape[0]
        #locationsNonZero = np.where(pairs[0]>0)
        #weightsTemp = 1/pairs[0][locationsNonZero]
        #weights = (weightsTemp/np.sum(weightsTemp))

        #mesh['LineSources'][pairs[1][0]] = 90000
        #mesh['LineSources'][pairs[1][locationsNonZero]] = 90000*weights #[3:nPointsRadius]] = 90000*weights
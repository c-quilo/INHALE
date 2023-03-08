import numpy as np
from scipy.optimize import minimize

def dataAssimilation(mesh, optionDA, sensorField, zeroField, radius):
    print('DA...')
    print(radius)
    def J(v):
        vT = np.transpose(v)
        vTv = np.dot(vT, v)
        Vv = np.dot(V, v)
        Jmis = np.subtract(Vv, d)
        invR = np.reciprocal(R)
        JmisT = np.transpose(Jmis)
        RJmis = JmisT.copy()
        J1 = invR * np.dot(Jmis, RJmis)
        Jv = (vTv + J1) / 2
        return Jv

    def gradJ(v):
        Vv = np.dot(V, v)
        Jmis = np.subtract(Vv, d)
        invR = np.reciprocal(R)
        g1 = Jmis.copy()
        VT = np.transpose(V)
        g2 = np.dot(VT, g1)
        gg2 = np.multiply(invR, g2)
        ggJ = v + gg2
        return ggJ

    #Rvalues = np.linspace(0.1, 1, 10)
    #V = np.cov(linSim)
    #Vvalues = np.linspace(1, 0.1, 10)
    linSim = mesh['allSources']
    linObs = mesh['sensorField']
    if optionDA == 'Dual':
        linSimTemp = linSim[linObs>0]
        linObsTemp = linObs[linObs>0]
    elif optionDA == 'Everything':
        linSimTemp = linSim
        linObsTemp = linObs
    #Vvalues = np.linspace(0.5, 0.5, 1)
    #Rvalues = (1 - Vvalues)
    V = 0.9
    R = 1 - V
    yobs = linObsTemp
    x0 = np.ones(linSimTemp.shape[0])
    Vin = 1/V
    v0 = np.dot(Vin, x0)

    VT = np.transpose(V)
    HxB = linSimTemp.copy()
    d = np.subtract(yobs, HxB)
    #t = time.time()
    res = minimize(J, v0, method='L-BFGS-B', jac=gradJ,
                    options={'disp': False})

    vDA = np.array([])
    vDA = res.x
    deltaxDA = np.dot(V,vDA)
    xDA_innov = linSimTemp + deltaxDA
    print(xDA_innov.shape)
    #if optionDA == 'Dual':
    #    print(linSim[linObs>0])
    #    linSim[linObs>0] = xDA_innov
    #    print(linSim[linObs>0])
    #    xDA_innov = linSim

    #xDA_innov = mesh['LineSources']
    #xDA_innov[linObs<0.1] = linSimTemp
    #if optionDA == 'Dual':
    #    xDA_innov[linObs > 0] = linSimTemp
    #elif optionDA == 'Everything':
    #    xDA_innov = linSimTemp
    #ug.AddScalarField('DAField_' + optionDA + ' ' + str(i) + ' r: ' + str(radius), xDA_innov)
    
    DA = zeroField.copy()
    SimSensors = zeroField.copy()

    DA[linObs>0] = xDA_innov
    SimSensors[linObs>0] = linSimTemp
    linSim[linObs>0] = xDA_innov
    #print(np.mean(DA-sensorField))
    #print(np.mean(SimSensors - sensorField))

    #ug.AddScalarField('sensorField_' + str(i) + ' r: ' + str(radius), sensorField)
    #ug.AddScalarField('DAField_' + str(i) + ' r: ' + str(radius), linSim)
    #ug.AddScalarField('simSensorsField_' + str(i) + ' r: ' + str(radius), SimSensors)
    #ug.AddScalarField('DAdiff_' + str(i) + ' r: ' + str(radius), DA - sensorField)
    #ug.AddScalarField('Simdiff_' + str(i) + ' r: ' + str(radius), SimSensors - sensorField)

    #print('Saving...')
    #ug.Write(filename)

    #print('Done: Window ' + str(i) + ' ' + str(hour_start) + ':' + str(minute_start) + ' to ' + str(hour_end) + ':' + str(minute_end))
    print(np.mean(linSimTemp) - np.mean(sensorField[linObs > 0]))
    print(np.square(linSimTemp - sensorField[linObs>0]).mean())
    print(np.mean(xDA_innov) - np.mean(sensorField[linObs > 0]))
    print(np.square(xDA_innov - sensorField[linObs>0]).mean())
    print(np.mean(sensorField[linObs > 0]))
    print(np.square(sensorField[linObs>0]).mean())

    print(np.mean(sensorField[linObs > 0]))
    return linSim
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:40:02 2017
"""

import numpy as np
import matplotlib.pyplot as plt
from instruments import Instrument
from lockin import Lockin
import time

path = r'D:/Grupo1-2do2017/'

loc_resource = 'GPIB0::8::INSTR' 
gen_resource = 'USB0::0x0699::0x0346::C034167::INSTR'

loc = Lockin(resource=loc_resource ,
             backend='', 
             path=path)

gen = Instrument(resource=gen_resource,
                 backend='', 
                 path=path)

#%% Medición 00 a 08

n = 500 + 1
prom = 1
Vi = -2.0
Vf = 2.0
V = np.linspace(Vi, Vf, n)
X = np.zeros(n)
Y = np.zeros(n)
R = np.zeros(n)

loc.auxiliar_outs.AuxOut1 = V[0]
#time.sleep(10)

for i, v in enumerate(V):
    loc.auxiliar_outs.AuxOut1 = v
    for j in range(prom):
        time.sleep(0.3)
        x, y, r = loc.adquisition.read_multiple('X', 'Y', 'R', log=False)
        X[i] += x
        Y[i] += y
        R[i] += r
    X[i] = X[i] / prom
    Y[i] = Y[i] / prom
    R[i] = R[i] / prom

plt.plot(V,X)
loc.auxiliar_outs.AuxOut1 = V[0]
    
#%% Medición 09

n = 200 + 1
prom = 1
Vi = 2.0
Vf = 4.0
V = np.linspace(Vi, Vf, n)
X = np.zeros(n)
Y = np.zeros(n)

#time.sleep(10)

for i, v in enumerate(V):
    gen.write('VOLT:HIGH {:.4f}'.format(v))
    for j in range(prom):
        time.sleep(0.3)
        x, y = loc.adquisition.read_multiple('X', 'Y', log=False)
        X[i] += x
        Y[i] += y

    X[i] = X[i] / prom
    Y[i] = Y[i] / prom

plt.plot(V,X)

#%% Medición 10-11

n = 100 + 1
Vi = -2.0
Vf = 2.0
V = np.linspace(Vi, Vf, n)
VLED = np.asarray([2.0, 3.0, 4.0], dtype=float)
X = np.zeros([5, n])
Y = np.zeros([5, n])

loc.auxiliar_outs.AuxOut1 = V[0]
gen.write('VOLT:HIGH {:.4f}'.format(VLED[0]))
time.sleep(5)

for i, v in enumerate(V):
    loc.auxiliar_outs.AuxOut1 = v
    for j, vled in enumerate(VLED):
        gen.write('VOLT:HIGH {:.4f}'.format(vled))
        time.sleep(0.3)
        X[j][i], Y[j][i] = loc.adquisition.read_multiple('X', 'Y', log=False)

for i in range(len(VLED)):
    plt.plot(V,X[i])
    
loc.auxiliar_outs.AuxOut1 = V[0]

#%% Medición 12-20

n = 100 + 1
prom = 1
Vi = -2.0
Vf = 2.0
V = np.linspace(Vi, Vf, n)
X = np.zeros(n)
Y = np.zeros(n)

loc.auxiliar_outs.AuxOut1 = V[0]
#time.sleep(10)

for i, v in enumerate(V):
    loc.auxiliar_outs.AuxOut1 = v
    for j in range(prom):
        time.sleep(0.3)
        x, y = loc.adquisition.read_multiple('X', 'Y', log=False)
        X[i] += x
        Y[i] += y
    X[i] = X[i] / prom
    Y[i] = Y[i] / prom

plt.plot(V,X)
loc.auxiliar_outs.AuxOut1 = V[0]
    
    
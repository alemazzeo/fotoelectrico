#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 00:41:47 2017

@author: batman
"""

import matplotlib
matplotlib.use('Qt5Agg')

from cycler import cycler
import numpy as np
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from analisis import mediciones, espectros, ventana_espectros
from analisis import ajuste

plt.ion()

#Led azul:
fig, ax = plt.subplots(1)

for i in range(5):
    v_ret, v_foto = mediciones['10']
    v_foto0 = v_foto[i] - np.mean(v_foto[i][v_ret < -1.0])
    pol, r = ajuste(v_ret, v_foto0, 0.0, 2.0)
    ax.plot(v_ret, v_foto0, 'o')
    ax.plot(v_ret, pol(v_ret))
    ax.grid()
    for i in range(10):
        if r.real[i] > 0.2 and r.real[i]< 0.4:
            print(r.real[i])

ax.set_xlim(0.0, 2.0)
ax.set_ylim(-1e-6, 1.1e-5)
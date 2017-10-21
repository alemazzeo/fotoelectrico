# -*- coding: utf-8 -*-

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

mediciones_blanco = [mediciones[str(i)] for i in range(14, 19)]
espectros_blanco = [espectros[str(i)] for i in range(14, 19)]

fig, ax = plt.subplots(2)

for medicion, espectro in zip(mediciones_blanco, espectros_blanco):
    v_ret, v_foto = medicion
    long_onda, intensidad = espectro

    pol = ajuste(v_ret, v_foto, xmin=1.3, xmax=np.inf, grado=1)

    ax[0].plot(v_ret, pol(v_ret), color='k', ls=':')
    ax[0].plot(v_ret, v_foto, marker='o', ls='')
    ax[1].plot(long_onda, intensidad)

ax[0].set_xlim(-1.0, 2.0)
ax[0].set_ylim(-1e-6, 2.5e-5)


fig, ax = plt.subplots(2)

for medicion, espectro in zip(mediciones_blanco, espectros_blanco):
    v_ret, v_foto = medicion
    long_onda, intensidad = espectro

    pol = ajuste(v_ret, v_foto, xmin=0, xmax=2.0, grado=10)

    ax[0].plot(v_ret, pol(v_ret), color='k', ls=':')
    ax[0].plot(v_ret, v_foto, marker='o', ls='')
    ax[1].plot(long_onda, intensidad)

ax[0].set_xlim(-0.2, 2.0)
ax[0].set_ylim(-1e-6, 2.5e-5)

# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Qt5Agg')

from cycler import cycler
import numpy as np
from scipy import signal
from scipy.optimize import curve_fit
from scipy.interpolate import InterpolatedUnivariateSpline as spline
import matplotlib.pyplot as plt

from analisis import mediciones, espectros, ventana_espectros

plt.ion()

mediciones_blanco = [mediciones[str(i)] for i in range(14, 19)]
espectros_blanco = [espectros[str(i)] for i in range(14, 19)]

fig, ax = plt.subplots(2)

areas = []
pendientes = []


def ajuste(x, y, xmin, xmax, grado=3):
    assert xmin < xmax
    mask = (x < xmax) * (x > xmin)
    p = np.polyfit(x[mask], y[mask], grado)
    pol = np.poly1d(p)
    return pol


def sensibilidad(smooth=0.001, plot=False):
    puntos = np.asarray([[300, 0.08],
                         [320, 0.24],
                         [330, 0.60],
                         [340, 0.76],
                         [352, 0.88],
                         [370, 0.94],
                         [405, 1.00],
                         [440, 0.94],
                         [460, 0.88],
                         [480, 0.80],
                         [500, 0.68],
                         [600, 0.12],
                         [610, 0.07],
                         [630, 0.04],
                         [650, 0.02],
                         [670, 0.01],
                         [700, 0.00],
                         [710, 0.00],
                         [720, 0.00],
                         [730, 0.00],
                         [740, 0.00],
                         [750, 0.00],
                         [800, 0.00],
                         [900, 0.00]])

    s = spline(puntos.T[0], puntos.T[1])
    s.set_smoothing_factor(smooth)
    if plot:
        fig, ax = plt.subplots(1)
        x = np.linspace(300, 700)
        ax.plot(puntos.T[0], puntos.T[1], 'o')
        ax.plot(x, s(x))

    return s


for medicion, espectro in zip(mediciones_blanco, espectros_blanco):
    v_ret, v_foto = medicion
    long_onda, intensidad = espectro

    lmin, lmax = [400, 700]
    mask = (long_onda > lmin) * (long_onda < lmax)

    long_onda = long_onda[mask]
    intensidad = intensidad[mask]

    pol = ajuste(v_ret, v_foto, xmin=1.5, xmax=np.inf, grado=1)

    ax[0].plot(v_ret, pol(v_ret), color='k', ls=':')
    ax[0].plot(v_ret, v_foto, marker='o', ls='')
    ax[1].plot(long_onda, intensidad, color='k', ls='--', lw=0.5, )

    s = sensibilidad()(long_onda + 50)
    h = intensidad * s

    ax[1].plot(long_onda, s * 0.15, color='k')
    ax[1].plot(long_onda, h)

    area = np.trapz(h)
    pendiente = pol[1] * 1e6

    areas.append(area)
    pendientes.append(pendiente)

    print('Area: {:f}\nPendiente: {:f}\n\n'.format(area, pendiente))

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

# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
from scipy import signal
from scipy.optimize import curve_fit
from scipy.interpolate import InterpolatedUnivariateSpline as spline
import matplotlib.pyplot as plt

from analisis import mediciones, espectros, ventana_espectros

# CONFIGURACIONES POR DEFECTO

# Figura (tamaño)
plt.rc('figure', figsize=(8, 6))

# Ticks (tamaño de la fuente)
plt.rc(('xtick', 'ytick'), labelsize=14)

# Bordes de la figura (visibles o no)
plt.rc('axes.spines', left=True, bottom=True, top=False, right=False)

# Leyenda (tamaño de la fuenta y ubicación)
plt.rc('legend', fontsize=14, loc='best')

# Ejes (tamaño de la fuente)
plt.rc('axes', labelsize=15)

plt.ion()

# DATOS

v_ret = mediciones['14'][0]
long_onda = espectros['14'][0]

lmin, lmax = [400, 700]
mask = (long_onda > lmin) * (long_onda < lmax)
long_onda = long_onda[mask]

v_foto = [mediciones[str(i)][1] * 1e6 for i in range(14, 19)]
intensidad = [espectros[str(i)][1][mask] - 0.01 for i in range(14, 19)]
intensidad = [x * (x > 0.0) for x in intensidad]

# FUNCIONES


def ajuste(x, y, xmin, xmax, grado=3):
    assert xmin < xmax
    mask = (x < xmax) * (x > xmin)
    p = np.polyfit(x[mask], y[mask], grado)
    pol = np.poly1d(p)
    return pol


def sensibilidad(long_onda, inicio=300, fin=700,
                 smooth=0.001, plot=False):
    puntos = np.asarray([[300, 0.08], [320, 0.24], [330, 0.60],
                         [340, 0.76], [352, 0.88], [370, 0.94],
                         [405, 1.00], [440, 0.94], [460, 0.88],
                         [480, 0.80], [500, 0.68], [600, 0.12],
                         [610, 0.07], [630, 0.04], [650, 0.02],
                         [670, 0.01], [700, 0.00], [710, 0.00],
                         [720, 0.00], [730, 0.00], [740, 0.00],
                         [750, 0.00], [800, 0.00], [900, 0.00]])

    s = spline(puntos.T[0], puntos.T[1])
    s.set_smoothing_factor(smooth)
    a = long_onda[0] + 300 - inicio
    b = long_onda[-1] + 700 - fin
    x = np.linspace(a, b, len(long_onda))

    if plot:
        fig, ax = plt.subplots(1)
        ax.plot(puntos.T[0], puntos.T[1], 'o')
        ax.plot(x, s(x))
        ax.plot(long_onda, s(x), 'k')

    return s(x)


def plot_pendientes(ax=None, xmin=1.0, xmax=np.inf):

    if ax is None:
        fig, ax = plt.subplots(1)

    pendientes = list()

    for i in range(5):
        ax.plot(v_ret, v_foto[i], ls='', marker='o')
        recta = ajuste(v_ret, v_foto[i], xmin=xmin, xmax=xmax, grado=1)
        ax.plot(v_ret, recta(v_ret), color='k', ls=':')
        pendientes.append(recta[1])

        texto = r'a={:05.2f}, b={:3.2f}'.format(recta[1], recta[0])
        ax.annotate(texto, xy=(2.0, v_foto[i][-1]),
                    xytext=(2.1, v_foto[i][-1]), fontsize=14,
                    verticalalignment='center')

        ax.set_ylim([0.0, 22.0])
        ax.set_xlim([0.70, 2.90])

        ax.set_xlabel(r'Potencial de frenado (V)')
        ax.set_ylabel(r'Fotocorriente $\propto$ V ($\mu$V)')

    return pendientes / pendientes[1]


def plot_espectros_corregidos(s, ax=None, plot_sensibilidad=True):

    if ax is None:
        fig, ax = plt.subplots(1)

    if plot_sensibilidad:
        ax.plot(long_onda, s * 0.15, color='k')

    areas = list()

    for i in range(5):
        ax.plot(long_onda, intensidad[i], ls=':', color='k', lw=0.5)
        h = intensidad[i] * s
        h = h * (h > 0)
        ax.plot(long_onda, h)
        areas.append(np.trapz(h))

    ax.set_xlabel(r'Long. de onda ($nm$)')
    ax.set_ylabel(r'Intensidad')

    return areas / areas[1]


def areas(long_onda, inicio, fin):
    areas = list()
    s = sensibilidad(long_onda, inicio=inicio, fin=fin)
    for i in range(5):
        h = intensidad[i] * s
        h = h * (h > 0)
        areas.append(np.trapz(h))

    return areas / areas[1]


def ajuste_sensibilidad(x0=1.0):
    pendientes = plot_pendientes(xmin=x0)
    popt, cov = curve_fit(areas, long_onda, pendientes, p0=[300, 700],
                          bounds=([100, 350], [550, 700]))
    return popt, pendientes, areas(long_onda, *popt)


# PROGRAMA PRINCIPAL

if __name__ == "__main__":
    fig, ax = plt.subplots(2)
    plot_pendientes(ax=ax[0])
    s = sensibilidad(long_onda, inicio=300, fin=650)
    plot_espectros_corregidos(s, ax=ax[1])

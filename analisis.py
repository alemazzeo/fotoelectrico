# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from datos import mediciones, espectros, ventana_espectros


def sol_monocromatica(v_ret, v_ret0, m, offset=1.5e-6):
    return (v_ret - v_ret0) * m * (v_ret > v_ret0) + offset


def ajuste(v_ret, v_foto, xmin, xmax):
    mask = (v_ret < xmax) * (v_ret > xmin)
    x = v_ret[mask]
    y = v_foto[mask]
    p = np.polyfit(x, y, 10)
    pol = np.poly1d(p)
    r = pol.r
    return pol, r


def ver_medicion(nombre):
    v_ret, v_foto = mediciones[nombre]
    fig, ax = plt.subplots(1)
    ax.plot(v_ret, v_foto)


def ver_espectro(nombre):
    long_onda, intensidad = espectros[nombre]
    fig, ax = plt.subplots(1)
    ax.plot(long_onda, intensidad)
    ax.set_xlim(ventana_espectros[nombre])


plt.ion()


def ver_juntos(nombre, espectro=''):
    fig, ax = plt.subplots(2)
    v_ret, v_foto = mediciones[nombre]
    long_onda, intensidad = espectros[nombre + espectro]

    ax[0].plot(v_ret, v_foto)
    ax[0].plot(v_ret, sol_monocromatica(v_ret, 0.7, 0.75e-5) + v_foto[0])
    ax[1].plot(long_onda, intensidad)


def ver_led_azul():
    fig, ax = plt.subplots(2)
    for i in range(5, 9):
        v_ret, v_foto = mediciones['0' + str(i)]
        long_onda, intensidad = espectros['0' + str(i) + 'A']

        ax[0].plot(v_ret, v_foto)
        ax[1].plot(long_onda, intensidad)
        # ax[1].set_xlim(ventana_espectros[str(i)])


def ver_led_blanco():
    fig, ax = plt.subplots(2)
    for i in range(14, 21):
        v_ret, v_foto = mediciones[str(i)]
        long_onda, intensidad = espectros[str(i)]

        ax[0].plot(v_ret, v_foto)
        ax[1].plot(long_onda, intensidad)
        # ax[1].set_xlim(ventana_espectros[str(i)])


def ver_barrido_led():
    fig, ax = plt.subplots(2)
    for i, letra in enumerate(['A', 'B', 'C', 'D', 'E']):
        v_ret, v_foto = mediciones['10']
        long_onda, intensidad = espectros['10' + letra]
        ax[0].plot(v_ret, v_foto[i])
        ax[1].plot(long_onda, intensidad)


def ver_barrido_led2():
    fig, ax = plt.subplots(2)
    for i, letra in enumerate(['A', 'B', 'C']):
        v_ret, v_foto = mediciones['11']
        long_onda, intensidad = espectros['11' + letra]
        ax[0].plot(v_ret, v_foto[i])
        ax[1].plot(long_onda, intensidad)


def ver_variacion_temporal():
    fig, ax = plt.subplots(2)
    for i in range(0, 6):
        v_ret, v_foto = mediciones['0' + str(i)]
        long_onda, intensidad = espectros['0' + str(i) + 'A']

        ax[0].plot(v_ret, v_foto)
        ax[1].plot(long_onda, intensidad)

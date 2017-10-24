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
import matplotlib.lines as mlines

from analisis import mediciones, espectros, ventana_espectros
from analisis import ajuste

plt.ion()

#%%
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
#%%
# Led azul:
fig, ax = plt.subplots(2)
fig.subplots_adjust(left=0.10, right=0.94, top=0.95, bottom=0.10,
                    hspace=0.40, wspace=0.2)


for i in range(3, -1, -1):
    letras = ['B', 'C', 'D', 'E']
    v_ret, v_foto = mediciones['10']
    long_onda, intensidad = espectros['10' + letras[i]]
    v_foto0 = v_foto[i] - np.mean(v_foto[i][v_ret < -1.0])
    pol, r = ajuste(v_ret, v_foto0, 0.0, 2.0)
    u = i * 0.5 + 2.5
    ax[0].plot(v_ret, v_foto0 * (1e6), 'o', ms=8,
               mec='None', label='{:.2f} V'.format(u))
    ax[0].plot(v_ret, pol(v_ret) * (1e6), color='k')
    ax[0].axhline(linestyle=':', color='k')
    ax[0].set_xlabel(r'Voltaje (V)')
    ax[0].set_ylabel(r'Fotocorriente $\propto$ V ($\mu$V)')

    for j in range(10):
        if r.real[j] > 0.2 and r.real[j] < 0.4:
            print(r.real[j])

    ax[1].plot(long_onda, intensidad)
    ax[1].set_xlabel(r'Long. de onda ($nm$)')
    ax[1].set_ylabel('Intensidad (u.a)\n')
    ax[1].set_yticks([])

ax[0].plot([], [], '-', color='k', label='Ajustes')
ax[0].legend(loc='best', ncol=1)
ax[0].set_xlim(0.2, 1.0)
ax[0].set_ylim(-0.5, 4.0)
ax[1].set_xlim(460, 480)


#%%
# Led azul para otras frecuencias:

fig, ax = plt.subplots(2)
fig.subplots_adjust(left=0.10, right=0.94, top=0.95, bottom=0.10,
                    hspace=0.40, wspace=0.2)

long_onda, intensidad = espectros['05' + 'A']
letras = [r'$\alpha$', r'$\beta$', r'$\gamma$', r'$\delta$']
posiciones = [1212, 1247, 1285, 1371]
longitud = [long_onda[i] for i in posiciones]
alturas = [0.028, 0.083, 0.134, 0.048]


for i in range(5, 9):
    v_ret, v_foto = mediciones['0' + str(i)]
    long_onda, intensidad = espectros['0' + str(i) + 'A']
    v_foto0 = v_foto - np.mean(v_foto[v_ret < -1.0])
    pol, r = ajuste(v_ret, v_foto0, 0.0, 2.0)
    ax[0].plot(v_ret[::4], v_foto0[::4] * (1e6), 'o', ms=8, alpha=0.7,
               mec='None')
    ax[0].plot(v_ret, pol(v_ret) * (1e6), color='k', zorder=10, lw=1.5)
    ax[0].axhline(linestyle=':', color='k', zorder=10)
    ax[0].set_xlabel(r'Voltaje (V)')
    ax[0].set_ylabel(r'Fotocorriente $\propto$ V ($\mu$V)')
    for j in range(10):
        if r.real[j] > 0.2 and r.real[j] < 0.4:
            print(r.real[j])

    texto = '{:s}'.format(letras[i - 5])
    ax[0].annotate(texto, xy=(2.0, v_foto[-10] * (1e6) - 1),
                   xytext=(2.05, v_foto[-10] * (1e6) - 1), fontsize=14,
                   verticalalignment='center')

    ax[1].plot(long_onda, intensidad)
    ax[1].set_xlabel(r'Long. de onda ($nm$)')
    ax[1].set_ylabel('Intensidad (u.a)\n')
    ax[1].set_yticks([])

    ax[1].annotate(letras[i - 5], xy=(longitud[i - 5], alturas[i - 5]),
                   xytext=(longitud[i - 5], alturas[i - 5] + 0.01),
                   fontsize=14, horizontalalignment='center')


ax[0].set_xlim(0.2, 2.15)
ax[0].set_ylim(-0.5, 17.0)
ax[1].set_xlim(445, 505)

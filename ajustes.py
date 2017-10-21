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
#Led azul:
fig, ax = plt.subplots(1)

for i in range(4):
    v_ret, v_foto = mediciones['10']
    v_foto0 = v_foto[i] - np.mean(v_foto[i][v_ret < -1.0])
    pol, r = ajuste(v_ret, v_foto0, 0.0, 2.0)
    u = i*0.5+2.5
    ax.plot(v_ret, v_foto0*(1e6), 'o', ms = 8, mec='None', label= '{:.2f} V'.format(u))
    ax.plot(v_ret, pol(v_ret)*(1e6), color='k')
    ax.axhline(linestyle=':', color='k')
    ax.set_xlabel(r'Voltaje (V)')
    ax.set_ylabel(r'Fotocorriente $\propto$ V ($\mu$V)')
#    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.legend(loc='best', ncol=2)
    for i in range(10):
        if r.real[i] > 0.2 and r.real[i]< 0.4:
            print(r.real[i])

ax.set_xlim(0.2, 1.0)
ax.set_ylim(-0.5, 4.0)
import numpy as np
import os

ruta_mediciones = {}
mediciones = {}
ruta_espectros = {}
espectros = {}


def corrige_fase(x, y):
    theta = np.arctan2(y, x)
    x_ = + np.cos(theta) * x + np.sin(theta) * y
    # y_ = - np.sin(theta) * x + np.cos(theta) * y
    return x_


for path, subdirs, files in os.walk('.'):
    for name in files:
        nombre, extension = os.path.splitext(name)
        ruta = os.path.join(path, name)

        if extension == '.npy':
            ruta_mediciones.update({nombre[8:]: ruta})

            m = int(nombre[8:])

            if m in range(0, 9):
                X, Y = np.load(ruta)
                V = np.linspace(-2.0, 2.0, 501)
                x = corrige_fase(X, Y)

            elif m == 9:
                X, Y = np.load(ruta)
                V = np.linspace(2.0, 4.0, 201)
                x = corrige_fase(X, Y)

            elif m == 10:
                X, Y = np.load(ruta)
                V = np.linspace(-2.0, 2.0, 101)
                x = np.asarray([corrige_fase(X[i], Y[i]) for i in range(1,5)])

            elif m == 11:
                X, Y = np.load(ruta)
                V = np.linspace(-2.0, 2.0, 101)
                x = np.asarray([corrige_fase(X[i], Y[i]) for i in range(3)])

            elif m in [12, 13]:
                X, Y = np.load(ruta)
                V = np.linspace(-2.0, 2.0, 201)
                x = corrige_fase(X, Y)

            elif m >= 14:
                X, Y = np.load(ruta)
                V = np.linspace(-2.0, 2.0, 101)
                x = corrige_fase(X, Y)

            medicion = [V, x]
            mediciones.update({nombre[8:]: medicion})

        elif extension == '.csv':
            ruta_espectros.update({nombre[8:]: os.path.join(path, name)})
            with open(ruta) as f:
                datos = [dato for dato in f]
            espectro = np.loadtxt(datos[33:-2], delimiter=',', comments='#')
            espectros.update({nombre[8:]: espectro.T})

ventana_espectros = {'01A': [455, 480],
                     '01B': [455, 480],
                     '02A': [455, 480],
                     '02B': [455, 480],
                     '03A': [455, 480],
                     '04B': [455, 480],
                     '04A': [455, 480],
                     '05B': [455, 480],
                     '05A': [455, 480],
                     '06B': [440, 480],
                     '06A': [440, 480],
                     '07A': [470, 510],
                     '07B': [470, 510],
                     '08A': [455, 485],
                     '08B': [455, 485],
                     '09': [450, 490],
                     '10A': [455, 485],
                     '10B': [455, 485],
                     '10C': [455, 485],
                     '10D': [455, 485],
                     '10E': [455, 485],
                     '11A': [580, 660],
                     '11B': [580, 660],
                     '11C': [580, 660],
                     '12': [580, 680],
                     '13': [580, 660],
                     '14': [420, 470],
                     '15': [440, 500],
                     '16': [460, 560],
                     '17': [500, 600],
                     '18': [560, 700],
                     '19': [600, 750],
                     '20': [620, 800]}

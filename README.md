# Práctica 2 - Efecto fotoeléctrico

## Contenido

### Adquisición
El archivo [fotoelectrico.py](./fotoelectrico.py) contiene los scripts utilizados para la adquisición.
El mismo tiene dependencia con los archivos del repositorio [instruments](https://github.com/labo5-grupo1/instruments)

Se añadieron recientemente copias en este repositorio para evitar la pérdida de compatibilidad
([instruments.py](./instruments.py), [lockin.py](./lockin.py), [lockin_commands.py](./lockin_commands.py) y [tools.py](./tools.py))

Además, en la carpeta [Otros](./Otros) se encuentran los archivos .html de las terminales de ipython.

### Mediciones
Las carpetas llamadas [LED AZUL](./LED%20AZUL/), [LED ROJO](./LED%20ROJO/) y [LED BLANCO](./LED%20BLANCO/) contienen dos tipos de archivos:
* **Las mediciones del Lock-In (tipo .npy)**, guardadas como X e Y en general (para curvas simultáneas se tienen matrices).
* **Los espectros (tipo .csv)**, adquiridos mediante el [software](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=OSA) de Thorlabs.

El archivo [datos.py](./datos.py) se encarga de facilitar el acceso a las mediciones mencionadas, como muestra el siguiente ejemplo:
```
from datos import mediciones, espectros
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2)
v_ret, v_foto = mediciones['10']
long_onda, intensidad = espectros['10A']

ax[0].plot(v_ret, v_foto)
ax[1].plot(long_onda, intensidad)
```

### Análisis
El archivo [analisis.py](./analisis.py) sirvió para pruebas básicas y generales.
Todas las figuras, con sus correspondientes ajustes, pueden ser regeneradas a partir de [ajustes.py](./ajustes.py) y [espectros.py](./espectros.py).

### Figuras
Todas las [figuras](./Figuras) del informe están disponibles para consulta.

### Informe
Se incluyó en el repositorio una [copia](./informe.pdf) de informe entregado.

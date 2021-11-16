# Optimizacion de Programacion
Software para la programación de pedidos transportados hacia las estaciones de servicio.

## Dependencias del software
Ejecutar los siguientes comandos, usando Python 3.8.0 como base.
```
pip install pandas
pip install plotly
pip install requests
pip install openpyxl
pip install osmnx
pip install networkx
pip install cryptography
pip install geopy
pip install dash
```

## Distancias y tiempos obtenidos del algoritmo TSP
### Usando coordenadas de entrada
Distancia total: 830.414300663492 Km
Tiempo total: 114.82 segundos

### Usando distancias de entrada
Distancia total: 808.8525647069278 Km
Tiempo total: 111.34 segundos

## Rutas por tipo de mapa
Las rutas por cada unidad se pueden mostrar en los siguientes tipos de mapas.

### Modelo "basic"
![](imagenes_mapas/rutas-basic.png "Modelo basic")

### Modelo "streets"
![](imagenes_mapas/rutas-streets.png "Modelo streets")

### Modelo "outdoors"
![](imagenes_mapas/rutas-outdoors.png "Modelo outdoors")

### Modelo "light"
![](imagenes_mapas/rutas-light.png "Modelo light")

### Modelo "dark"
![](imagenes_mapas/rutas-dark.png "Modelo dark")

### Modelo "satellite"
![](imagenes_mapas/rutas-satellite.png "Modelo satellite")

### Modelo "satellite-streets"
![](imagenes_mapas/rutas-satellite-streets.png "Modelo satellite-streets")

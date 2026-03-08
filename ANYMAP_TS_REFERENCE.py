#!/usr/bin/env python3
"""
[REFERENCIA CRÍTICA] ANYMAP-TS vs FOLIUM
Este archivo muestra cómo usar correctamente AnyMap TS. 
PROHIBIDO USAR FOLIUM EN ESTE PROYECTO.
"""

import anymap_ts as anymap
import pandas as pd
import json

# 1. Configuración del Mapa (MapLibre GL JS)
m = anymap.Map(
    center=[-3.6867, 40.4740], # Madrid (Parque Norte)
    zoom=16,
    style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
)

# 2. Añadir datos (GeoJSON)
puntos_interes = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Entrada Principal", "type": "park"},
            "geometry": {"type": "Point", "coordinates": [-3.6870, 40.4745]}
        },
        {
            "type": "Feature",
            "properties": {"name": "Lago", "type": "water"},
            "geometry": {"type": "Point", "coordinates": [-3.6855, 40.4735]}
        }
    ]
}

# En AnyMap TS, usamos add_geojson para capas vectoriales
m.add_geojson(
    data=puntos_interes,
    layer_id="parque_puntos",
    paint={
        "circle-radius": 8,
        "circle-color": "#007cbf"
    }
)

# 3. Mostrar el mapa (Solo funciona en entornos AnyWidget/Jupyter/Voila)
# m # En un notebook
print("Mapa AnyMap TS configurado correctamente con 2 capas.")

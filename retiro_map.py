# -*- coding: utf-8 -*-
from anymap_ts import Map
import json
from pathlib import Path

# Coordenadas del Parque del Retiro
centro = [40.4140, -3.6826]
zoom = 16

# Crea un mapa
m = Map(center=centro, zoom=zoom)

# Añade una capa base (OpenStreetMap)
m.add_basemap("OpenStreetMap")

# Crea un archivo GeoJSON de prueba (reemplaza esto con el GeoJSON real)
geojson_prueba = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[-3.685, 40.412], [-3.680, 40.412], [-3.680, 40.417], [-3.685, 40.417], [-3.685, 40.412]]
                ]
            }
        }
    ]
}

# Guarda el GeoJSON de prueba en un archivo
geojson_path = 'data/parque_retiro.geojson'
Path('data').mkdir(exist_ok=True)
with open(geojson_path, 'w') as f:
    json.dump(geojson_prueba, f)

# Añade una capa vectorial (GeoJSON)
with open(geojson_path, 'r') as f:
    geojson_data = json.load(f)

m.add_vector(geojson_data, name="Parque del Retiro")

# Añade control de dibujo
m.add_draw_control()

# Genera el HTML
m.to_html("retiro_map.html")

print("Mapa generado en retiro_map.html")

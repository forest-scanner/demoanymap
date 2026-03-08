# -*- coding: utf-8 -*-
import anywidget
import traitlets
import json
from pathlib import Path

# Define la clase AnyMap
class AnyMap(anywidget.AnyWidget):
    _esm = Path('./script.js').read_text()
    value = traitlets.Dict({}).tag(sync=True)

# Función para crear el mapa
def crear_mapa_alcazaba(geojson_path, center_coordinates, zoom_level):
    # Carga el GeoJSON
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)

    # Crea el mapa
    mapa = AnyMap(
        value={
            'center': center_coordinates,
            'zoom': zoom_level,
            'geojson': geojson_data,
        }
    )
    return mapa

if __name__ == '__main__':
    # Coordenadas de ejemplo (ajusta esto con las coordenadas reales del Parque Alcazaba)
    centro = [ -3.7038, 40.4168 ] # Ejemplo: Madrid
    zoom = 14 # Ajusta el zoom

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
                        [[-3.705, 40.415], [-3.700, 40.415], [-3.700, 40.420], [-3.705, 40.420], [-3.705, 40.415]]
                    ]
                }
            }
        ]
    }

    # Guarda el GeoJSON de prueba en un archivo
    geojson_path = 'data/parque_alcazaba.geojson'
    Path('data').mkdir(exist_ok=True)
    with open(geojson_path, 'w') as f:
        json.dump(geojson_prueba, f)

    # Crea el mapa
    mapa = crear_mapa_alcazaba(geojson_path, centro, zoom)

    # Muestra el mapa (esto se mostrará en un entorno Jupyter o similar)
    print(mapa)

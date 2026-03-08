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
def crear_mapa_casa_de_campo(geojson_path, center_coordinates, zoom_level):
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
    # Coordenadas de la Casa de Campo en Madrid
    centro = [40.413669, -3.731778]
    zoom = 16

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
                        [[-3.735, 40.410], [-3.730, 40.410], [-3.730, 40.415], [-3.735, 40.415], [-3.735, 40.410]]
                    ]
                }
            }
        ]
    }

    # Guarda el GeoJSON de prueba en un archivo
    geojson_path = 'data/casa_de_campo.geojson'
    Path('data').mkdir(exist_ok=True)
    with open(geojson_path, 'w') as f:
        json.dump(geojson_prueba, f)

    # Crea el mapa
    mapa = crear_mapa_casa_de_campo(geojson_path, centro, zoom)

    # Muestra el mapa (esto se mostrará en un entorno Jupyter o similar)
    print(mapa)

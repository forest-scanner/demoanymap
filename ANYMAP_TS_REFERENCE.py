#!/usr/bin/env python3
"""
[REFERENCIA CRÍTICA] AnyMap-TS — Código correcto de la librería opengeos/anymap-ts

⚠️ PROHIBIDO:
  - class MiMapa(anywidget.AnyWidget)  ← MAL, esto es una plantilla vacía
  - import anywidget                   ← MAL, la librería YA lo hace internamente

✅ CORRECTO:
  - from anymap_ts import Map          ← La librería provee clases listas
  - m.to_html("visor.html")           ← Exporta HTML standalone
"""

# ============================================================
# EJEMPLO 1: MapLibre (motor por defecto)
# ============================================================
from anymap_ts import Map

m = Map(center=[-3.6867, 40.4740], zoom=16)
m.add_basemap("OpenStreetMap")
m.add_draw_control()

# Añadir datos vectoriales (GeoJSON)
puntos_interes = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Entrada Principal", "tipo": "acceso"},
            "geometry": {"type": "Point", "coordinates": [-3.6870, 40.4745]}
        },
        {
            "type": "Feature",
            "properties": {"name": "Lago", "tipo": "agua"},
            "geometry": {"type": "Point", "coordinates": [-3.6855, 40.4735]}
        }
    ]
}

m.add_vector(puntos_interes, name="parque_puntos")
m.fly_to(-3.6867, 40.4740, zoom=17)
m.to_html("demoanymap/visor_parque_norte.html", title="Parque Norte - Madrid")

# ============================================================
# EJEMPLO 2: DeckGL (capas de alto rendimiento)
# ============================================================
from anymap_ts import DeckGLMap

deck = DeckGLMap(center=[-3.70, 40.42], zoom=12)
deck.add_basemap("CartoDB.DarkMatter")

# Capa de hexágonos para densidad
datos = [{"coordinates": [-3.70, 40.42], "value": 100}]
deck.add_hexagon_layer(data=datos, radius=500, extruded=True)
deck.to_html("demoanymap/visor_deckgl.html")

# ============================================================
# EJEMPLO 3: Cesium (globo 3D)
# ============================================================
from anymap_ts import CesiumMap

cesium = CesiumMap(center=[-3.70, 40.42], zoom=10)
cesium.add_basemap("OpenStreetMap")
cesium.set_terrain()
cesium.fly_to(-3.6867, 40.4740, height=5000, heading=45, pitch=-30)
cesium.to_html("demoanymap/visor_cesium.html")

# ============================================================
# EJEMPLO 4: Con GeoPandas (datos vectoriales reales)
# ============================================================
# import geopandas as gpd
# gdf = gpd.read_file("data/parcelas.geojson")
# m = Map(center=[-3.70, 40.42], zoom=14)
# m.add_basemap("OpenStreetMap")
# m.add_vector(gdf, name="parcelas")
# m.to_html("demoanymap/visor_parcelas.html")

print("✅ Referencia AnyMap-TS correcta. Todos los ejemplos usan 'from anymap_ts import ...'")

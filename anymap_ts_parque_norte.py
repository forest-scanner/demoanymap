# Código en Python básico de AnyMap TS del Parque Norte de Madrid

import anymap_ts as anymap

# Mapa del Parque Norte usando AnyMap TS
m = anymap.Map(
    center=[-3.6867, 40.4740],
    zoom=16
)

# Añadir punto de interés
m.add_geojson({
    "type": "Feature",
    "properties": {"name": "Punto Central"},
    "geometry": {"type": "Point", "coordinates": [-3.6867, 40.4740]}
})

print("Mapa AnyMap TS del Parque Norte generado.")
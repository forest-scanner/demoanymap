# Mapa básico de AnyMap TS del Parque Norte de Madrid

import folium

# Crear mapa
mapa = folium.Map(location=[40.468326, -3.693048], zoom_start=15)

# Agregar capas al mapa
folium.Marker([40.468326, -3.693048], popup='Parque Norte').add_to(mapa)

# Guardar mapa como HTML
mapa.save('mapa_parque_norte.html')
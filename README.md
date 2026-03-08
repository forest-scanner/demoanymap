# AnyMap TS - Estándar de Visualización

Este proyecto utiliza **única y exclusivamente** AnyMap TS para visualizaciones geoespaciales.

## 🚫 REGLA DE ORO
**PROHIBIDO EL USO DE FOLIUM.**
Cualquier código que use Folium será considerado obsoleto y debe ser migrado a AnyMap TS.

## Tecnologías Core
- **AnyMap TS**: Basado en `anywidget` y `MapLibre GL JS`.
- **AnyWidget**: Para comunicación bidireccional Python ↔ JavaScript.
- **Turf.js**: Para análisis espacial en el lado del cliente (frontend).
- **MapLibre GL GeoEditor**: Para edición geométrica interactiva.

## Ejemplo de Referencia
Consulta `ANYMAP_TS_REFERENCE.py` para ver el patrón de uso correcto.

## Cómo migrar de Folium
| Folium | AnyMap TS |
|--------|-----------|
| `folium.Map()` | `anymap_ts.Map()` |
| `folium.Marker()` | `m.add_geojson()` o `m.add_marker()` |
| `mapa.add_to(m)` | `m.add_layer()` |
| `mapa.save()` | AnyMap se rinde dinámicamente vía anywidget |

---
**Autor:** OpenGravity Expert Identity
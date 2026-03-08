import * as anywidget from 'anywidget';
import * as maplibregl from 'maplibre-gl';

anywidget.register('AnyMap', (container, { value }) => {
  const map = new maplibregl.Map({
    container: container,
    style: 'https://demotiles.maplibre.org/style.json',
    center: value.center,
    zoom: value.zoom,
  });

  if (value.geojson) {
    map.on('load', () => {
      map.addSource('parque-alcazaba', {
        type: 'geojson',
        data: value.geojson,
      });

      map.addLayer({
        id: 'parque-alcazaba-fill',
        type: 'fill',
        source: 'parque-alcazaba',
        paint: {
          'fill-color': '#008000',
          'fill-opacity': 0.5,
        },
      });
    });
  }

  return () => map.remove();
});

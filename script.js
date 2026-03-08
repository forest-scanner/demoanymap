import * as anywidget from 'anywidget';
import * as maplibregl from 'maplibre-gl';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [0, 0],
  zoom: 2
});

anywidget.register('AnyMap', (container) => {
  container.appendChild(map.getCanvas());
  return () => map.remove();
});

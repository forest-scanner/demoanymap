import { AnyMap } from 'anymap';

const map = new AnyMap({
  container: 'map',
  center: [40.549067, -3.686581],
  zoom: 15,
  layers: [
    {
      type: 'ortofoto',
      url: 'https://ortofotos.munimadrid.es/ortofotos/ortho/{z}/{x}/{y}.jpg',
      maxZoom: 19,
    },
  ],
});
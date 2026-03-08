from anymap_ts import Map

m = Map(center=[40.4140, -3.6826], zoom=15)
m.add_basemap("OpenStreetMap")
m.to_html("demoanymap/visor_retiro.html")

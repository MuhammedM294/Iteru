from ipyleaflet import TileLayer, basemaps, basemap_to_tiles

from ipywidgets import*


basemaps = {
    "Google Road Map": TileLayer(
        url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Road Map",
    ),
    "Google Terrain": TileLayer(
        url="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Terrain",
    ),
    "Google Hybrid": TileLayer(
        url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Hybrid",
    ),
    "ESRI": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Satellite",
    ),
    "Esri Ocean": TileLayer(
        url="https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Ocean",
    ),
    "Esri Satellite": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Satellite",
    ),
    "Esri Standard": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Standard",
    ),
    "Esri Terrain": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Terrain",
    ),
    "Esri Transportation": TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Transportation",
    ),
    "Esri Topo World": TileLayer(
        url="https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Topo World",
    ),
    "Esri National Geographic": TileLayer(
        url="http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri National Geographic",
    ),
    "Esri Shaded Relief": TileLayer(
        url="https://services.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Shaded Relief",
    ),
    "Esri Physical Map": TileLayer(
        url="https://services.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        name="Esri Physical Map",
    ),

    "Open Street Map (Black&White)": basemap_to_tiles(basemaps.OpenStreetMap.BlackAndWhite),

    "Open Street Map (France)": basemap_to_tiles(basemaps.OpenStreetMap.France),

    "Open Street Map Hot": basemap_to_tiles(basemaps.OpenStreetMap.HOT),
      
    "Open Topo Map": basemap_to_tiles(basemaps.OpenTopoMap),

    "Gaode Normal": basemap_to_tiles(basemaps.Gaode.Normal),

    "Gaode Satellite":  basemap_to_tiles(basemaps.Gaode.Satellite),

    "Hydda Full":  basemap_to_tiles(basemaps.Hydda.Full),

    "Hydda Base": basemap_to_tiles(basemaps.Hydda.Base),

    "Esri World Street Map":  basemap_to_tiles(basemaps.Esri.WorldStreetMap),

    "Esri Delorme":  basemap_to_tiles(basemaps.Esri.DeLorme),

    "Esri World Topo Map":  basemap_to_tiles(basemaps.Esri.WorldTopoMap),

    "Esri World Imagery " : basemap_to_tiles(basemaps.Esri.WorldImagery),

    "Esri NatGeoWorld Map": basemap_to_tiles (basemaps.Esri.NatGeoWorldMap),

    "HikeBike.HikeBike":  basemap_to_tiles(basemaps.HikeBike.HikeBike), 

    "MtbMap":  basemap_to_tiles(basemaps.MtbMap), 

    "CartoDB Positron": basemap_to_tiles(basemaps.CartoDB.Positron), 

    "CartoDB DarkMatter":   basemap_to_tiles(basemaps.CartoDB.DarkMatter), 

    "NASAGIBS ModisTerraTrueColorCR":  basemap_to_tiles(basemaps.NASAGIBS.ModisTerraTrueColorCR) , 

    "NASAGIBS ModisTerraBands367CR":  basemap_to_tiles(basemaps.NASAGIBS.ModisTerraBands367CR), 

    "NASAGIBS ModisTerraBands721CR":  basemap_to_tiles(basemaps.NASAGIBS.ModisTerraBands721CR), 

    "NASAGIBS ModisAquaTrueColorCR":  basemap_to_tiles(basemaps.NASAGIBS.ModisAquaTrueColorCR), 

    "NASAGIBS ModisAquaBands721CR":  basemap_to_tiles(basemaps.NASAGIBS.ModisAquaBands721CR), 

    "NASAGIBS ViirsTrueColorCR":   basemap_to_tiles(basemaps.NASAGIBS.ViirsTrueColorCR),

    "NASAGIBS ViirsEarthAtNight2012": basemap_to_tiles(basemaps.NASAGIBS.ViirsEarthAtNight2012),

    "Strava.All":  basemap_to_tiles(basemaps.Strava.All), 

    "Strava.Ride":  basemap_to_tiles(basemaps.Strava.Ride), 

    "Strava Run": basemap_to_tiles(basemaps.Strava.Run), 

    "Strava Water":   basemap_to_tiles(basemaps.Strava.Water), 

    "Strava.Winter": basemap_to_tiles(basemaps.Strava.Winter), 

    "Stamen Terrain":  basemap_to_tiles(basemaps.Stamen.Terrain), 

    "Stamen Toner":  basemap_to_tiles(basemaps.Stamen.Toner) , 

    "Stamen Watercolor":  basemap_to_tiles(basemaps.Stamen.Watercolor)
} 


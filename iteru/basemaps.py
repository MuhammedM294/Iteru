
basemaps = {
    "Google Road Map": TileLayer(
        url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Maps",
    ),
    "Google Terrain": TileLayer(
        url="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Terrain",
    ),
    "Google Hybrid": TileLayer(
        url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attribution="Google",
        name="Google Satellite",
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
    )
} 
import ee 
from ipywidgets import *


terrain_dataset = { 

    
    "AHN Netherlands 0.5m DEM, Interpolated":
                                                     ee.Image("AHN/AHN2_05M_INT") , 

    "AHN Netherlands 0.5m DEM, Non-Interpolated":
                                                     ee.Image("AHN/AHN2_05M_NON"), 

    "AHN Netherlands 0.5m DEM, Raw Samples":
                                                     ee.Image("AHN/AHN2_05M_RUW"),

    "DEM-H: Australian SRTM Hydrologically Enforced Digital Elevation Model":

                                                     ee.Image("AU/GA/DEM_1SEC/v10/DEM-H"),
    
    "DEM-S: Australian Smoothed Digital Elevation Model":

                                                      ee.Image("AU/GA/DEM_1SEC/v10/DEM-S"), 

    "SRTM Digital Elevation Data Version 4":

                                                     ee.Image("CGIAR/SRTM90_V4")      ,

    "CryoSat-2 Antarctica 1km DEM":

                                                      ee.Image("CPOM/CryoSat2/ANTARCTICA_DEM"),

    "Global ALOS CHILI (Continuous Heat-Insolation Load Index)":

                                                      ee.Image("CSP/ERGo/1_0/Global/ALOS_CHILI"),

    "Global ALOS Landforms":

                                                      ee.Image("CSP/ERGo/1_0/Global/ALOS_landforms"),

    "Global ALOS mTPI (Multi-Scale Topographic Position Index)":

                                                      ee.Image("CSP/ERGo/1_0/Global/ALOS_mTPI"),

    "Global ALOS Topographic Diversity":

                                                      ee.Image("CSP/ERGo/1_0/Global/ALOS_topoDiversity"),
                                                    
   "Global SRTM CHILI (Continuous Heat-Insolation Load Index)":

                                                     ee.Image("CSP/ERGo/1_0/Global/SRTM_CHILI"),

    "Global SRTM Landforms":
     
                                                     ee.Image("CSP/ERGo/1_0/Global/SRTM_landforms"),

    "Global SRTM mTPI (Multi-Scale Topographic Position Index)":

                                                     ee.Image("CSP/ERGo/1_0/Global/SRTM_mTPI"),

    "Global SRTM Topographic Diversity":

                                                     ee.Image("CSP/ERGo/1_0/Global/SRTM_topoDiversity"),

    "US NED CHILI (Continuous Heat-Insolation Load Index)":

                                                     ee.Image("CSP/ERGo/1_0/US/CHILI"),

     "US NED Landforms":

                                                     ee.Image("CSP/ERGo/1_0/US/landforms"),

    "US Lithology":

                                                     ee.Image("CSP/ERGo/1_0/US/lithology"),

    "US NED mTPI (Multi-Scale Topographic Position Index)":

                                                     ee.Image("CSP/ERGo/1_0/US/mTPI"),

    "US NED Physiographic Diversity ":

                                                   ee.Image("CSP/ERGo/1_0/US/physioDiversity"),

    "US Physiography":

                                                   ee.Image("CSP/ERGo/1_0/US/physiography"),

    "US NED Topographic Diversity ":

                                                   ee.Image("CSP/ERGo/1_0/US/topoDiversity"),
    
    "MERIT DEM: Multi-Error-Removed Improved-Terrain DEM":

                                                    ee.Image("MERIT/DEM/v1_0_3"),
    
    "MERIT Hydro: Global Hydrography Datasets":

                                                    ee.Image("MERIT/Hydro/v1_0_1"),

    "MERIT Hydro: Supplementary Visualization Layers":

                                                    ee.Image("MERIT/Hydro_reduced/v1_0_1"),

    "AG100: ASTER Global Emissivity Dataset 100-meter V003":

                                                     ee.Image("NASA/ASTER_GED/AG100_003"),

    "NASADEM: NASA NASADEM Digital Elevation 30m":

                                                     ee.Image("NASA/NASADEM_HGT/001"),

    "ETOPO1: Global 1 Arc-Minute Elevation":

                                                     ee.Image("NOAA/NGDC/ETOPO1"),

    
    "USGS 3DEP National Map Seamless 1/3 Arc-Second (10m)":

                                                     ee.Image("USGS/3DEP/10m"),

    "GMTED2010: Global Multi-resolution Terrain Elevation Data 2010":

                                                      ee.Image("USGS/GMTED2010"),

    "GTOPO30: Global 30 Arc-Second Elevation":

                                                      ee.Image("USGS/GTOPO30"),

    "NASA SRTM Digital Elevation 30m":

                                                      ee.Image("USGS/SRTMGL1_003"),
    
    "WWF HydroSHEDS Hydrologically Conditioned DEM, 3 Arc-Seconds":

                                                      ee.Image("WWF/HydroSHEDS/03CONDEM"),

    "WWF HydroSHEDS Void-Filled DEM, 3 Arc-Seconds":

                                                     ee.Image("WWF/HydroSHEDS/03VFDEM"),

    "WWF HydroSHEDS Hydrologically Conditioned DEM, 15 Arc-Seconds":

                                                     ee.Image("WWF/HydroSHEDS/15CONDEM"),

    "WWF HydroSHEDS Hydrologically Conditioned DEM, 30 Arc-Seconds":

                                                      ee.Image("WWF/HydroSHEDS/30CONDEM"),

    "Australian 5M DEM": 

                                                     ee.ImageCollection("AU/GA/AUSTRALIA_5M_DEM"),                                               

    "HYCOM: Hybrid Coordinate Ocean Model, Sea Surface Elevation":

                                                   ee.ImageCollection("HYCOM/sea_surface_elevation"),

    "ALOS DSM: Global 30m":

                                                   ee.ImageCollection("JAXA/ALOS/AW3D30/V3_2"),
    "Canadian Digital Elevation Model":

                                                     ee.ImageCollection("NRCan/CDEM")


}


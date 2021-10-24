import ee 
from .iteru import *



terrain = { 

    
    "AHN Netherlands 0.5m DEM, Interpolated":
                                                     ee.Image("AHN/AHN2_05M_INT") , 

    "AHN Netherlands 0.5m DEM, Non-Interpolated":
                                                     ee.Image("AHN/AHN2_05M_NON"), 

    "AHN Netherlands 0.5m DEM, Raw Samples":
                                                     ee.Image("AHN/AHN2_05M_RUW"),

    "Australian 5M DEM": 

                                                     ee.ImageCollection("AU/GA/AUSTRALIA_5M_DEM"),

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

    "HYCOM: Hybrid Coordinate Ocean Model, Sea Surface Elevation":

                                                   ee.ImageCollection("HYCOM/sea_surface_elevation"),

    "ALOS DSM: Global 30m":

                                                   ee.ImageCollection("JAXA/ALOS/AW3D30/V3_2")

                                                       
                                                    

}
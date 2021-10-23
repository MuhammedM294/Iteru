import ee 

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

                                                     ee.Image("CGIAR/SRTM90_V4"),
    "CryoSat-2 Antarctica 1km DEM":

                                                     ee.Image("CPOM/CryoSat2/ANTARCTICA_DEM"),

    "Global ALOS CHILI (Continuous Heat-Insolation Load Index)":

                                                     ee.Image("CSP/ERGo/1_0/Global/ALOS_CHILI"),

    "Global ALOS Landforms":
                                                     ee.Image("CSP/ERGo/1_0/Global/ALOS_landforms")
                                                    

}
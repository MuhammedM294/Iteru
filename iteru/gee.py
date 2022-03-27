""" A Main Module for Google Earth Engine Python API Functions """

import ee
from ipywidgets import *
import ipyleaflet
from IPython.display import display
import datetime
from .common import *


def ee_tilelayer(ee_object, vis_params=None, name=''):

    ee_object_id = ee_object.getMapId(vis_params)

    ee_object_tile = ipyleaflet.TileLayer(

        url=ee_object_id['tile_fetcher'].url_format,
        attribution='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    )
    return ee_object_tile


def get_vis_params(collection):
    """A fucntion to get the visualiztions paramters of GEE ImageCollection Feature

    Args:
        collection ([ImageCollection]): [GEE ImageColelction]

    Returns:
        [dict]: [Visualization paramters ]
    """
    min = float(collection.getInfo()['properties']['visualization_0_min'])
    max = float(collection.getInfo()['properties']['visualization_0_max'])
    bands = collection.getInfo(
    )['properties']['visualization_0_bands'].split(',')
    return {'min': min, 'max': max, 'bands': bands}


def add_dates_to_imgcol(img):
    return img.set({"DATE": ee.Date(img.get("system:time_start")).format('YYYY-MM-dd')})


def get_imgCol_dates(col):
    col = col.map(add_dates_to_imgcol)
    return col.aggregate_array('DATE').getInfo()


def get_imgCol_dates_dict(col):

    dates_dict = {formated_date: date for formated_date, date in zip(
        get_imgCol_dates(col), col.aggregate_array('system:time_start').getInfo())}

    return dates_dict


def dates_params(startYear=2020, startMonth=6, startDay=1, endYear=2022, endMonth=3, endDay=1):

    if all(isinstance(i, int) for i in [startYear, startMonth, startDay, endYear, endMonth, endDay]):

        valid_startDate = datetime.date(2020, 1, 1)
        valid_endDate = datetime.date.today()
        startDate = datetime.date(startYear, startMonth, startDay)
        ee_startDate = f'{startYear}-{startMonth}-{startDay}'
        endDate = datetime.date(endYear, endMonth, endDay)
        ee_endDate = f'{endYear}-{endMonth}-{endDay}'

        if (valid_endDate >= startDate >= valid_startDate) and (valid_endDate >= endDate >= valid_startDate):
            pass
        else:
            try:
                raise Exception(
                    f'The start Date and the end Date should be between {valid_startDate} and {valid_endDate}')
            except Exception as e:
                print(e)
            return

        if (endDate - startDate).days < 0:
            try:
                raise Exception('The start Date should be before the end date')
            except Exception as e:
                print(e)
            return

        if 0 <= (endDate - startDate).days < 30:
            try:
                raise Exception(
                    'It should be at least one month between the start date and the end date')
            except Exception as e:
                print(e)
            return

        return list([startDate, endDate, ee_startDate, ee_endDate])

    else:
        try:
            raise Exception('The date parameters input should be integer')
        except Exception as e:
            print(e)
        return


def get_dates_sequence(start_date, end_date, time_delta=30):

    days = [start_date]

    while start_date < end_date:
        end_day = start_date + datetime.timedelta(days=time_delta)
        days.append(end_day)
        start_date = end_day

    while (end_date - days[-1]).days < 30:
        days.pop()

    days_dates = [f'{date.year}-{date.month}-{date.day}' for date in days]

    return days_dates


def addRatioBand(img):
    ratio_band = img.select('VV').divide(img.select('VH')).rename('VV/VH')

    return img.addBands(ratio_band)


def filterSpeckles(img):

    VH_smooth = img.select('VH').focal_median(
        100, 'circle', 'meters').rename('VH_Filtered')

    return img.addBands(VH_smooth)


def water_classify_threshold(col, threshold):

    def water_classify(img):

        VH_Filtered = img.select('VH_Filtered')
        water = VH_Filtered.lt(threshold).rename('water')
        water_mask = water.updateMask(water).rename('water_mask')

        return img.addBands([water, water_mask])

    return col.map(water_classify)


def rgb_water_mosaic(img):

    img_rgb = img.visualize(
        **{'min': [-35, -35, 0], 'max': [0, 0, 5], 'bands': ['VV', 'VH', 'VV/VH']})

    water_vis = img.select('Water_mask').visualize(
        **{'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']})

    mosaic = ee.ImageCollection([img_rgb, water_vis]).mosaic()

    return mosaic.copyProperties(img, img.propertyNames())


def S1_SAR_col(aoi, startYear, startMonth, startDay, endYear, endMonth, endDay, temp_freq=None):

    try:

        if aoi is None or not isinstance(aoi, ee.Geometry):

            raise Exception('The Study Area should ee.Geomtery')

    except Exception as e:

        print(e)

        return

    else:

        try:

            datesVars = dates_params(
                startYear, startMonth, startDay, endYear, endMonth, endDay)

        except Exception as e:
            print(e)
            return
        else:

            if datesVars:

                try:

                    SAR = ee.ImageCollection('COPERNICUS/S1_GRD')\
                        .filter(ee.Filter.equals('relativeOrbitNumber_start', 50))\
                        .filter(ee.Filter.eq('instrumentMode', 'IW'))\
                        .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))\
                        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
                        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
                        .filter(ee.Filter.eq('resolution_meters', 10))\
                        .filterBounds(aoi)\
                        .filterDate(datesVars[2], datesVars[3])\
                        .select(['VV', 'VH'])\
                        .map(addRatioBand)

                except Exception:

                    print('Error with Sentinel-1 SAR GRD ImageCollection filtering')
                    return

                else:
                    if temp_freq is None:

                        dates_sequence = get_imgCol_dates(SAR)

                        return [SAR, dates_sequence]

                    else:
                        try:

                            if temp_freq == 'monthly':

                                time_delta = 30

                                dates_sequence = get_dates_sequence(
                                    start_date=datesVars[0], end_date=datesVars[1], time_delta=30)

                            elif temp_freq == 'quarterly':

                                time_delta = 90

                                dates_sequence = get_dates_sequence(
                                    start_date=datesVars[0], end_date=datesVars[1], time_delta=90)

                            else:

                                raise Exception(
                                    'Invalid temporal frequency input')

                        except Exception as e:
                            print(e)
                            return
                        else:

                            def get_images_sequence(day):

                                start_day = ee.Date(day)
                                end_day = start_day.advance(time_delta, 'day')
                                image = SAR.filterDate(start_day, end_day).median()\
                                    .set({'start_day': start_day.format('YYYY-MM-dd')})\
                                    .set({'end_day': end_day.format('YYYY-MM-dd')})
                                return image

                            images = ee.List(dates_sequence).map(
                                get_images_sequence)

                            SAR = ee.ImageCollection.fromImages(images)

                            return [SAR, dates_sequence]


def SAR_timeseries_url(col, aoi, vis_method='rgb', water_threshold=-25, frame_per_second=2, crs='EPSG:3857', dimensions=900):

    try:
        if isinstance(col, ee.ImageCollection):
            pass
        else:
            raise Exception('The input should be ee.ImageCollection')

    except Exception as e:
        print(e)

    try:
        if isinstance(aoi, ee.Geometry):
            pass
        else:
            raise Exception('The input should be ee.Geometry')

    except Exception as e:
        print(e)

    palette = None
    vis_min = -35,
    vis_max = 5,

    try:
        if vis_method == 'rgb':

            vis_min = [-35, -35, 0]
            vis_max = [0, 0, 5]
            bands = ['VV', 'VH', 'VV/VH']

        elif vis_method == 'single_band_VV':
            bands = ['VV']
            palette = ['#000000', '#FFFFFF']

        elif vis_method == 'single_band_VV_R':
            bands = ['VV']
            palette = ['#FFFFFF', '#000000']

        elif vis_method == 'single_band_VH':

            bands = ['VH']
            palette = ['#000000', '#FFFFFF']

        elif vis_method == 'single_band_VH_R':

            bands = ['VH']
            palette = ['#FFFFFF', '#000000']

        elif vis_method == 'water_mask':

            col = col.map(filterSpeckles)
            col = water_classify_threshold(col, water_threshold)
            bands = ['water_mask']
            palette = ['00FFFF', '0000FF']

        elif vis_method == 'rgb_water_mosaic':

            col = col.map(filterSpeckles)
            col = water_classify_threshold(col, water_threshold)
            col = col.map(rgb_water_mosaic)

            bands = ['vis-red', 'vis-green', 'vis-blue']
            vis_min = 0
            vis_max = 255
        else:
            raise Exception('Invalid visualization method input. The visualization method should be'
                            '"rgb","singl_band_VV","single_band_VH","water_mask" or "rgb_water_mosaic"')

    except Exception as e:
        print(e)
        return
    else:

        videoArgs = {
            'dimensions': dimensions,
            'region': aoi,
            'framesPerSecond': frame_per_second,
            'crs': crs,
            'min': vis_min,
            'max': vis_max,
            'bands': bands,
            'palette': palette

        }
        try:

            url = col.getVideoThumbURL(videoArgs)

            return url

        except Exception:

            print(
                'The number of requested images exceeded the memory limit.'
                'Please, redcue the time period or the GIF dimensions.')
            return


def calc_area(feature):

    area = feature.geometry().area(maxError=1)

    return feature.set({'Area': area})


def water_to_vector(img):

    water_mask = img.select('water_mask').clip(GERD_aoi)

    feature = ee.Image(1).updateMask(water_mask).reduceToVectors(
        geometry=water_mask.geometry(),
        crs='EPSG:32636',
        scale=10,
        geometryType='polygon',
        eightConnected=False,
        labelProperty='water_cover',
        bestEffort=True
    )
    feature = feature.map(calc_area)

    lake_feature = feature.sort('Area', False).first()

    lake_area = lake_feature.geometry().area(maxError=1)

    return ee.FeatureCollection(lake_feature).set({'Area': lake_area})\
        .copyProperties(img, img.propertyNames())\
        .copyProperties(lake_feature, lake_feature.propertyNames())


def max_water_ele(feature):

    lake_dem = elevation_dataset.clip(feature)

    max_ele = lake_dem.reduceRegion(
        reducer=ee.Reducer.max(),
        geometry=lake_dem.geometry(),
        scale=30,
        crs='EPSG:32636',
        maxPixels=1e11).get('DSM')
    return lake_dem.set({'Maximum_water_elevation': max_ele})


def water_vol(lake_dem):

    elevations = lake_dem.reduceRegion(
        reducer=ee.Reducer.toList(),
        geometry=lake_dem.geometry(),
        maxPixels=1e11,
        scale=30,
        crs='EPSG:32636',
        bestEffort=True
    ).get('DSM')

    elev_pixles_num = ee.List(elevations).length()

    elev_sum = ee.List(elevations).reduce(ee.Reducer.sum())

    stats = {'Pixels_number': elev_pixles_num,
             'Elevation_sum': elev_sum
             }

    return ee.Feature(None, stats)


def toDB(img):
    return ee.Image(img).log10().multiply(10.0)


def toNatural(img):
    return ee.Image(10.0).pow(img.select(0).divide(10.0))


def RefinedLee(img):

    weights3 = ee.List.repeat(ee.List.repeat(1, 3), 3)
    kernel3 = ee.Kernel.fixed(3, 3, weights3, 1, 1, False)

    mean3 = img.reduceNeighborhood(ee.Reducer.mean(), kernel3)
    variance3 = img.reduceNeighborhood(ee.Reducer.variance(), kernel3)

    sample_weights = ee.List([[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0],
                              [0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0,
                                                      0, 0, 0], [0, 1, 0, 1, 0, 1, 0],
                              [0, 0, 0, 0, 0, 0, 0]])
    sample_kernel = ee.Kernel.fixed(7, 7, sample_weights, 3, 3, False)

    sample_mean = mean3.neighborhoodToBands(sample_kernel)
    sample_var = variance3.neighborhoodToBands(sample_kernel)

    gradients = sample_mean.select(1).subtract(sample_mean.select(7)).abs()
    gradients = gradients.addBands(sample_mean.select(
        6).subtract(sample_mean.select(2)).abs())
    gradients = gradients.addBands(sample_mean.select(
        3).subtract(sample_mean.select(5)).abs())
    gradients = gradients.addBands(sample_mean.select(
        0).subtract(sample_mean.select(8)).abs())

    max_gradient = gradients.reduce(ee.Reducer.max())
    gradmask = gradients.eq(max_gradient)
    gradmask = gradmask.addBands(gradmask)

    directions = sample_mean.select(1).subtract(sample_mean.select(4)).gt(
        sample_mean.select(4).subtract(sample_mean.select(7))).multiply(1)
    directions = directions.addBands(sample_mean.select(6).subtract(sample_mean.select(
        4)).gt(sample_mean.select(4).subtract(sample_mean.select(2))).multiply(2))
    directions = directions.addBands(sample_mean.select(3).subtract(sample_mean.select(
        4)).gt(sample_mean.select(4).subtract(sample_mean.select(5))).multiply(3))
    directions = directions.addBands(sample_mean.select(0).subtract(sample_mean.select(
        4)).gt(sample_mean.select(4).subtract(sample_mean.select(8))).multiply(4))

    directions = directions.addBands(directions.select(0).Not().multiply(5))
    directions = directions.addBands(directions.select(1).Not().multiply(6))
    directions = directions.addBands(directions.select(2).Not().multiply(7))
    directions = directions.addBands(directions.select(3).Not().multiply(8))

    directions = directions.updateMask(gradmask)
    directions = directions.reduce(ee.Reducer.sum())

    sample_stats = sample_var.divide(sample_mean.multiply(sample_mean))
    sigmaV = sample_stats.toArray().arraySort().arraySlice(
        0, 0, 5).arrayReduce(ee.Reducer.mean(), [0])

    rect_weights = ee.List.repeat(ee.List.repeat(0, 7), 3).cat(
        ee.List.repeat(ee.List.repeat(1, 7), 4))

    diag_weights = ee.List([[1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0],
                            [1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1]])

    rect_kernel = ee.Kernel.fixed(7, 7, rect_weights, 3, 3, False)
    diag_kernel = ee.Kernel.fixed(7, 7, diag_weights, 3, 3, False)

    dir_mean = img.reduceNeighborhood(
        ee.Reducer.mean(), rect_kernel).updateMask(directions.eq(1))
    dir_var = img.reduceNeighborhood(
        ee.Reducer.variance(), rect_kernel).updateMask(directions.eq(1))

    dir_mean = dir_mean.addBands(img.reduceNeighborhood(
        ee.Reducer.mean(), diag_kernel).updateMask(directions.eq(2)))
    dir_var = dir_var.addBands(img.reduceNeighborhood(
        ee.Reducer.variance(), diag_kernel).updateMask(directions.eq(2)))

    for i in range(1, 4):
        dir_mean = dir_mean.addBands(img.reduceNeighborhood(
            ee.Reducer.mean(), rect_kernel.rotate(i)).updateMask(directions.eq(2*i+1)))
        dir_var = dir_var.addBands(img.reduceNeighborhood(
            ee.Reducer.variance(), rect_kernel.rotate(i)).updateMask(directions.eq(2*i+1)))
        dir_mean = dir_mean.addBands(img.reduceNeighborhood(
            ee.Reducer.mean(), diag_kernel.rotate(i)).updateMask(directions.eq(2*i+2)))
        dir_var = dir_var.addBands(img.reduceNeighborhood(
            ee.Reducer.variance(), diag_kernel.rotate(i)).updateMask(directions.eq(2*i+2)))

    dir_mean = dir_mean.reduce(ee.Reducer.sum())
    dir_var = dir_var.reduce(ee.Reducer.sum())

    varX = dir_var.subtract(dir_mean.multiply(
        dir_mean).multiply(sigmaV)).divide(sigmaV.add(1.0))
    b = varX.divide(dir_var)

    result = dir_mean.add(b.multiply(img.subtract(dir_mean)))

    return(result.arrayFlatten([['sum']]))


def apply_RefinedLee(img):

    VH_Filtered = ee.Image(
        toDB(RefinedLee(toNatural(img.select(['VH']))))).rename('VH_Filtered')

    return img.addBands(VH_Filtered)


def otsu(histogram):

    counts = ee.Array(ee.Dictionary(histogram).get('histogram'))
    means = ee.Array(ee.Dictionary(histogram).get('bucketMeans'))
    size = means.length().get([0])
    total = counts.reduce(ee.Reducer.sum(), [0]).get([0])
    sum = means.multiply(counts).reduce(ee.Reducer.sum(), [0]).get([0])
    mean = sum.divide(total)

    indices = ee.List.sequence(1, size)

    def BSS(i):
        aCounts = counts.slice(0, 0, i)
        aCount = aCounts.reduce(ee.Reducer.sum(), [0]).get([0])
        aMeans = means.slice(0, 0, i)
        aMean = (
            aMeans.multiply(aCounts)
            .reduce(ee.Reducer.sum(), [0])
            .get([0])
            .divide(aCount)
        )
        bCount = total.subtract(aCount)
        bMean = sum.subtract(aCount.multiply(aMean)).divide(bCount)
        return aCount.multiply(aMean.subtract(mean).pow(2)).add(
            bCount.multiply(bMean.subtract(mean).pow(2))
        )

    bss = indices.map(BSS)

    return means.sort(bss).get([-1])


def addOtsuThreshold(img):

    histogram = img.select('VH_Filtered').reduceRegion(
        reducer=ee.Reducer.histogram().combine(
            'mean', None, True).combine('variance', None, True),
        geometry=GERD_aoi,
        scale=10,
        bestEffort=True
    )
    otsu_threshold = otsu(histogram.get('VH_Filtered_histogram'))

    water = img.select('VH_Filtered').lt(otsu_threshold).selfMask()

    return water.set({"otsu_threshold": otsu_threshold})


def GERD_SAR_timelaspe(aoi=GERD_aoi,
                       startYear=2020,
                       startMonth=6,
                       startDay=1,
                       endYear=2022,
                       endMonth=3,
                       endDay=19,
                       temp_freq=None,
                       vis_method='rgb',
                       water_threshold=-25,
                       crs='EPSG:3857',
                       dimensions=900,
                       dates_font_size=25,
                       copywrite_font_size=15,
                       dates_font_color='red',
                       copywrite_font_color='black',
                       framesPerSecond=2,
                       ):
    try:
        SAR_col = S1_SAR_col(aoi, startYear, startMonth,
                             startDay, endYear, endMonth, endDay, temp_freq)

    except Exception as e:
        print(e)
        return
    else:
        if isinstance(SAR_col, list):
            SAR = SAR_col[0]
            dates_sequences = SAR_col[1]

            try:

                url = SAR_timeseries_url(
                    SAR, aoi, vis_method, water_threshold, framesPerSecond, crs, dimensions)

            except Exception as e:
                print(e)
                return

            else:
                if url:

                    out_gif = get_gif(url)

                    out_gif = add_text_to_gif(out_gif, dates_sequences,
                                              dates_font_size,
                                              copywrite_font_size,
                                              dates_font_color,
                                              copywrite_font_color,
                                              framesPerSecond)

                    return out_gif


def GERD_water_stats(aoi=GERD_aoi,
                     startYear=2020,
                     startMonth=6,
                     startDay=1,
                     endYear=2022,
                     endMonth=3,
                     endDay=15,
                     temp_freq='monthly',
                     water_threshold=-25,
                     water_area=True,
                     water_level=False,
                     water_volume=False,
                     ):

    try:
        SAR_col = S1_SAR_col(aoi, startYear, startMonth,
                             startDay, endYear, endMonth, endDay, temp_freq)

        if isinstance(SAR_col, list):
            SAR = SAR_col[0]
            dates_sequences = SAR_col[1]

    except Exception as e:
        print(e)
        return
    else:

        try:
            if not water_area and not water_level and not water_volume:

                raise Exception("Check at least one of stats to be calculated")

        except Exception as e:

            print(e)
            return

        else:

            try:
                water_stats = {}
                water_stats['image_date'] = dates_sequences
                if water_area:
                    SAR = SAR.map(filterSpeckles)
                    SAR = water_classify_threshold(SAR, water_threshold)
                    water_vectors = SAR.map(water_to_vector)

                    water_area = [
                        area / (1e6) for area in water_vectors.aggregate_array('Area').getInfo()]
                    water_stats['water_surface_area'] = water_area

                if water_level:
                    if not water_area:

                        SAR = SAR.map(filterSpeckles)
                        SAR = water_classify_threshold(SAR, water_threshold)
                        water_vectors = SAR.map(water_to_vector)

                    dems = water_vectors.map(max_water_ele)

                    max_elev = [elev for elev in dems.aggregate_array(
                        'Maximum_water_elevation').getInfo()]
                    water_stats['maximum_elevation'] = max_elev

                if water_volume:

                    if not water_area:
                        SAR = SAR.map(filterSpeckles)
                        SAR = water_classify_threshold(SAR, water_threshold)
                        water_vectors = SAR.map(water_to_vector)
                    if not water_level:
                        dems = water_vectors.map(max_water_ele)
                        max_elev = [elev for elev in dems.aggregate_array(
                            'Maximum_water_elevation').getInfo()]

                    volume_stats = dems.map(water_vol)
                    ele_sum = volume_stats.aggregate_array(
                        'Elevation_sum').getInfo()
                    pixel_num = volume_stats.aggregate_array(
                        'Pixels_number').getInfo()
                    volume = [((water_level*pixles_count-elevations_sum)*900)/(1e9)
                              for water_level, elevations_sum, pixles_count in zip(max_elev, ele_sum, pixel_num)]
                    water_stats['water_volume'] = volume

                return water_stats

            except:
                print('Error! Memory Limit Exceeded.')

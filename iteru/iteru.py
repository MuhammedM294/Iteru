"""The main module for the interactive mapping based on Google Earth Enigne Python API and Ipyleaflet Package """


from IPython.display import display
from .common import *
from .gui_widgets import *
from ipywidgets import *
from ipyleaflet.leaflet import TileLayer
import os
import string
from inspect import CORO_CREATED
import ipyleaflet
import ee
import datetime


class Map(ipyleaflet.Map):
    """ Inherting the Map class from Ipyleaflet with the all its methods and attributes

    """

    def __init__(self, **kwargs):

        Map.zoom_control = False
        self.basemap = basemaps_dataset["Google Hybrid"]
        if 'center' not in kwargs:
            kwargs['center'] = [27, 31]

        if 'zoom' not in kwargs:
            kwargs['zoom'] = 5

        if 'scroll_wheel_zoom' not in kwargs:
            kwargs['scroll_wheel_zoom'] = True

        if 'height' not in kwargs:
            self.layout.height = '500px'
        else:
            self.layout.height = kwargs['height']

        super().__init__(**kwargs)

        self.add_control(ipyleaflet.SearchControl(

            position="topleft",
            url='https://nominatim.openstreetmap.org/search?format=json&q={s}',
            zoom=10,
            marker=ipyleaflet.Marker(
                icon=ipyleaflet.AwesomeIcon(name="check",
                                            marker_color='green', icon_color='darkgreen')
            )
        )
        )

        self.add_control(ipyleaflet.ScaleControl(position='bottomleft'))

        self.add_control(ipyleaflet.LayersControl(position='topleft'))

        self.add_control(ipyleaflet.ZoomControl(position='topright'))

        self.add_control(ipyleaflet.FullScreenControl(position='topright'))

        draw_control = ipyleaflet.DrawControl(position='topright')

        draw_control.polyline = {
            "shapeOptions": {
                "color": "blue",
                "weight": 8,
                "opacity": 0.5
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "blue",
                "color": "red",
                "fillOpacity": 0.1
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "blue",
                "color": "red",
                "fillOpacity": 0.1
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "blue",
                "color": "red",
                "fillOpacity": 0.1
            }
        }

        self.add_control(draw_control)
        self.draw_control = draw_control
        self.last_draw = draw_control.last_draw
        self.last_action = draw_control.last_action

        def handle_draw(target, action, geo_json):
            self.last_draw = geo_json
            self.last_action = action
            if self.last_draw['geometry']['type'] == 'Polygon':
                self.aoi = ee.Geometry.Polygon(
                    self.last_draw['geometry']['coordinates'])
            elif self.last_draw['geometry']['type'] == 'Point':
                self.aoi = ee.Geometry.Point(
                    self.last_draw['geometry']['coordinates'])
            elif self.last_draw['geometry']['type'] == 'LineString':
                self.aoi = ee.Geometry.LineString(
                    self.last_draw['geometry']['coordinates'])

        self.draw_control.on_draw(handle_draw)

        measure = ipyleaflet.MeasureControl(
            position='topright',
            active_color='orange',
            primary_length_unit='kilometers',
            secondary_length_unit=('miles'),
            secondary_area_unit=('acres')
        )

        measure.add_area_unit('Sq Kilometers', 1e-6, 4)
        measure.primary_area_unit = ('Sq Kilometers')
        self.add_control(measure)

        self.add_control(basemap_tool_widget)
        self.add_control(terrain_dataset_tool_widget)
        self.add_control(TOC_widget)

        def add_to_map(change):
            if change.new:
                self.add_layer_widgets(change.new)

        basemaps.observe(add_to_map, names='value')
        terrain.observe(add_to_map, names='value')

        # add coordinates of the mousemove to the map
        def from_decimal_to_degree(angle):
            degrees = int(angle)
            minutes = (angle - degrees)*60
            seconds = (minutes - int(minutes)) * 60
            return f"{degrees}°{int(minutes)}'{seconds:.4f}”"

        coordinates = HTML()

        def handle_interaction(**kwargs):
            if kwargs.get('type') == 'mousemove':
                coordinates.value = f"""
                                    <b>Lat</b>: {from_decimal_to_degree(float(str(kwargs.get('coordinates')[0])))}
                                    <br>
                                    <b>Long</b>: {from_decimal_to_degree(float(str(kwargs.get('coordinates')[1])))}
                                    <br>
                                    <b>Zoom Level</b>: {int(self.zoom)}
                                    """
            if kwargs.get('type') == 'click':
                JAXA = ee.ImageCollection(
                    'JAXA/ALOS/AW3D30/V3_2').select('DSM').median()
                lat = float(str(kwargs.get('coordinates')[0]))
                long = float(str(kwargs.get('coordinates')[1]))
                point_elevation = JAXA.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=ee.Geometry.Point(long, lat),
                    scale=10,).getInfo()
                coordinates.value = f"""
                                    <b>Lat</b>: {from_decimal_to_degree(float(str(kwargs.get('coordinates')[0])))}
                                    <br>
                                    <b>Long</b>: {from_decimal_to_degree(float(str(kwargs.get('coordinates')[1])))}
                                    <br>
                                    <b>Zoom Level</b>: {int(self.zoom)}
                                    <br>
                                    <b>Elevation</b>:{point_elevation['DSM']}
                                    """

        self.on_interaction(handle_interaction)
        coordinates_widget = WidgetControl(
            widget=coordinates, position='bottomleft')
        self.add_control(coordinates_widget)

    def add_layer_widgets(self, object, vis_params=None, name=None):
        try:
            if isinstance(object, ee.Image) or isinstance(object, ee.ImageCollection) or (object, ee.FeatureCollection):
                layer = ee_tilelayer(object, vis_params)
                if name is None:
                    name = object.getInfo()['id']

            elif isinstance(object, TileLayer):
                layer = object
                if name is None:
                    name = object.name
        except:
            print('input layer is not supported ')

        try:
            self.add_layer(layer)

            close_button = Button(
                value=False,
                tooltip='Remove This Layer',
                icon='window-close',
                layout=Layout(width='32px', height='28px'),
            )

            layer_visibility = Checkbox(
                value=True,
                indent=False,
                layout=Layout(width='15px')
            )

            layer_name = Label(
                value=name,
                layout=Layout(width='150px', height='28px'),
                tooltip=name
            )
            opacity = FloatSlider(
                value=1,
                min=0,
                max=1,
                step=0.1,
                indent=False,
            )

            def change_layer_visibility(show_hide):
                layer.visible = show_hide

            def change_layer_opacity(Opacity):
                layer.opacity = Opacity

            def remove_layer(b):
                self.remove_layer(layer)
                close_button.close()
                opacity.close()
                layer_name.close()
                layer_visibility.close()

            opacity_slider = interactive(change_layer_opacity, Opacity=opacity)

            visibility_checkbox = interactive(
                change_layer_visibility, show_hide=layer_visibility)

            with TOC_out:
                display(
                    HBox([layer_visibility, layer_name, opacity, close_button]))

            close_button.on_click(remove_layer)

        except Exception:
            pass
            #print(f'layer already on the map: {layer}')

    def zoom_to(self, ee_object, zoom=8):

        try:
            lat = ee_object.geometry().centroid().getInfo()['coordinates'][1]
            long = ee_object.geometry().centroid().getInfo()['coordinates'][0]
            self.center = (lat, long)
            self.zoom = zoom
        except:
            self.center = (27, 31)
            self.zoom = 5
            print('Error: can not get the centroid of the Object')

    def add_ee_layer(self, ee_object, vis_params=None, name=''):

        map_id_dict = ee_object.getMapId(vis_params)

        ee_object_tile = ipyleaflet.TileLayer(

            url=map_id_dict['tile_fetcher'].url_format,
            attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
            name=name,
            overlay=True,
            control=True
        )
        self.add_layer(ee_object_tile)


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


def get_gif(url):

    import requests
    import os

    r = requests.get(url, stream=True)
    out_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    filename = "TimeSeries_" + random_string() + ".gif"
    out_gif = os.path.join(out_dir, filename)

    with open(out_gif, 'wb') as file:
        for chunk in r.iter_content(chunk_size=1024):
            file.write(chunk)

    return out_gif


def random_string(string_length=4):
    import random
    import string

    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(string_length))


def add_text_to_gif(out_gif, dates_list, dates_font_size=25, dates_font_color='red', framesPerSecond=4):

    from PIL import Image, ImageDraw, ImageFont, ImageSequence
    import io

    gif = Image.open(out_gif)
    count = gif.n_frames

    width, height = gif.size
    dates_text_xy = (int(0.001 * width), int(0.001 * height))
    copywrite_xy = (int(0.001 * width), int(0.95 * height))

    dates_text = dates_list
    copywrite = '©Muhammed Abdelaal, 2022'
    dates_text_font = ImageFont.truetype(
        r'C:\Users\muham\Downloads\News 705 Italic BT\News 705 Italic BT.ttf', dates_font_size)
    copywrite_font = ImageFont.truetype(
        r'C:\Users\muham\Downloads\News 705 Italic BT\News 705 Italic BT.ttf', 15)

    frames = []

    for index, frame in enumerate(ImageSequence.Iterator(gif)):
        frame = frame.convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text(dates_text_xy, dates_text[index],
                  fill=dates_font_color, font=dates_text_font)
        draw.text(copywrite_xy, copywrite, fill="black", font=copywrite_font)
        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        frames.append(frame)

    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000/framesPerSecond),
        loop=0,
        optimize=True,
    )


def display_gif(out_gif):

    from ipywidgets import Image

    out = Output()
    out.clear_output(wait=True)
    display(out)
    with out:
        with open(out_gif, 'rb') as file:
            image = file.read()
        display(Image(value=image))


def addRatioBand(img):
    ratio_band = img.select('VV').divide(img.select('VH')).rename('VV/VH')

    return img.addBands(ratio_band)


def dates_params(startYear=2022, startMonth=1, startDay=1, endYear=2022, endMonth=3, endDay=1):

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
        end_day = start_date + datetime.timedelta(days=24)
        days.append(end_day)
        start_date = end_day

    while (end_date - days[-1]).days < time_delta:
        days.pop()

    days_dates = [f'{date.year}-{date.month}-{date.day}' for date in days]

    return days_dates


def S1_SAR_col(startYear, startMonth, startDay, endYear, endMonth, endDay, temp_freq=None):

    try:
        aoi = ee.Geometry.Polygon([[[
            35.008243,
            10.522199
        ],
            [
            35.008243,
            11.266588
        ],
            [
            35.387092,
            11.266588
        ],
            [
            35.387092,
            10.522199
        ],
            [
            35.008243,
            10.522199
        ]]])

        if not isinstance(aoi, ee.Geometry):

            raise Exception('The Study Area should ee.Geomtery')

            return

    except Exception as e:

        print(e)
    try:

        datesVars = dates_params(
            startYear, startMonth, startDay, endYear, endMonth, endDay)

    except Exception as e:
        print(e)
        return

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

        except Exception as e:

            print('Error with Sentinel-1 image collection filtering')
            return

    if temp_freq is None:

        return SAR

    elif temp_freq == 'monthly':

        dates_sequence = get_dates_sequence(
            start_date=datesVars[0], end_date=datesVars[1], time_delta=30)

        def get_images_sequence(day):

            start_day = ee.Date(day)
            end_day = start_day.advance(1, 'month')
            image = SAR.filterDate(start_day, end_day).median()\
                       .set({'start_day': start_day.format('YYYY-MM-dd')})\
                       .set({'end_day': end_day.format('YYYY-MM-dd')})
            return image

        images = ee.List(dates_sequence).map(get_images_sequence)

        SAR = ee.ImageCollection.fromImages(images)

        return SAR


def SAR_timeseries_url(col, aoi, vis_method=None, frame_per_second=2, crs='EPSG:3857', dimensions=900):

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

    if vis_method is None:

        vis_min = [-25, -25, 0]
        vis_max = [0, 0, 5]
        bands = ['VV', 'VH', 'VV/VH']

    elif vis_method == 'single_band_VV':

        vis_min = -25,
        vis_max = 5,
        bands = ['VV']

    elif vis_method == 'single_band_VH':

        vis_min = -25,
        vis_max = 5,
        bands = ['VH']

    videoArgs = {

        'dimensions': dimensions,
        'region': aoi,
        'framesPerSecond': frame_per_second,
        'crs': crs,
        'min': vis_min,
        'max': vis_max,
        'bands': bands
    }

    try:

        url = col.getVideoThumbURL(videoArgs)

        return url

    except Exception:

        print('The number of requested images exceeded the memory limit. Please, redcue the dates limit')
        return

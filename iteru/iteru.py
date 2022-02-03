"""The main module for the interactive mapping based on Google Earth Enigne Python API and Ipyleaflet Package """


import os
import string
from inspect import CORO_CREATED
import ipyleaflet
import ee
from ipyleaflet.leaflet import TileLayer
from ipywidgets import *
from .gui_widgets import *
from .common import *
from IPython.display import display


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
        self.on_interaction(handle_interaction)
        coordinates_widget = WidgetControl(
            widget=coordinates, position='bottomleft')
        self.add_control(coordinates_widget)

    def add_layer_widgets(self, object, vis_params=None, name=None):
        try:
            if isinstance(object, ee.Image) or isinstance(object, ee.ImageCollection):
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


def get_dates_list(start_date, end_date, time_delta=30):

    import datetime

    days = [start_date]

    while start_date < end_date:
        end_day = start_date + datetime.timedelta(days=time_delta)
        days.append(end_day)
        start_date = end_day

    while (end_date - days[-1]).days < time_delta:
        days.pop()
    days_dates = []

    for date in days:
        days_dates.append(f'{date.year}-{date.month}-{date.day}')

    return days_dates


def sentinel_2_sr_timeseries(aoi, start_year=2021, start_month=1, start_day=1, end_year=2022, end_month=1, end_day=1,
                             time_delta=30, CLOUD_FILTER=40, CLD_PRB_THRESH=70, NIR_DRK_THRESH=0.15, CLD_PRJ_DIST=1,
                             BUFFER=50):
    import datetime

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)

    ee_start_date = f'{start_year}-{start_month}-{start_day}'
    ee_end_date = f'{end_year}-{end_month}-{end_day}'

    dates_list = get_dates_list(start_date, end_date, time_delta)

    def get_s2_sr_cld_col(aoi, ee_start_date, ee_end_date, CLOUD_FILTER):

        s2_sr_col = (ee.ImageCollection('COPERNICUS/S2_SR')
                     .filterBounds(aoi)
                     .filterDate(ee_start_date, ee_end_date)
                     .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', CLOUD_FILTER)))

        s2_cloudless_col = (ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')
                            .filterBounds(aoi)
                            .filterDate(ee_start_date, ee_end_date))

        return ee.ImageCollection(ee.Join.saveFirst('s2cloudless').apply(**{
            'primary': s2_sr_col,
            'secondary': s2_cloudless_col,
            'condition': ee.Filter.equals(**{
                'leftField': 'system:index',
                'rightField': 'system:index'
            })
        }))

    s2_sr_cld_col_eval = get_s2_sr_cld_col(
        aoi, ee_start_date, ee_end_date, CLOUD_FILTER)

    def add_cloud_bands(img):
        cld_prb = ee.Image(img.get('s2cloudless')).select('probability')
        is_cloud = cld_prb.gt(CLD_PRB_THRESH).rename('clouds')
        return img.addBands(ee.Image([cld_prb, is_cloud]))

    def add_shadow_bands(img):
        not_water = img.select('SCL').neq(6)

        SR_BAND_SCALE = 1e4
        dark_pixels = img.select('B8').lt(
            NIR_DRK_THRESH*SR_BAND_SCALE).multiply(not_water).rename('dark_pixels')

        shadow_azimuth = ee.Number(90).subtract(
            ee.Number(img.get('MEAN_SOLAR_AZIMUTH_ANGLE')))

        cld_proj = (img.select('clouds').directionalDistanceTransform(shadow_azimuth, CLD_PRJ_DIST*10)
                                        .reproject(**{'crs': img.select(0).projection(), 'scale': 100})
                                        .select('distance')
                                        .mask()
                                        .rename('cloud_transform'))

        shadows = cld_proj.multiply(dark_pixels).rename('shadows')

        return img.addBands(ee.Image([dark_pixels, cld_proj, shadows]))

    def add_cld_shdw_mask(img):
        img_cloud = add_cloud_bands(img)

        img_cloud_shadow = add_shadow_bands(img_cloud)

        is_cld_shdw = img_cloud_shadow.select('clouds').add(
            img_cloud_shadow.select('shadows')).gt(0)

        is_cld_shdw = (is_cld_shdw.focalMin(2).focalMax(BUFFER*2/20)
                       .reproject(**{'crs': img.select([0]).projection(), 'scale': 20})
                       .rename('cloudmask'))

        return img_cloud_shadow.addBands(is_cld_shdw)

    def apply_cld_shdw_mask(img):
        not_cld_shdw = img.select('cloudmask').Not()

        return img.select('B.*').updateMask(not_cld_shdw).clip(aoi)

    s2_sr_cld_col_eval = s2_sr_cld_col_eval.map(
        add_cld_shdw_mask).map(apply_cld_shdw_mask)

    def get_images(day_date):

        start_day = ee.Date(day_date)
        end_day = start_day.advance(time_delta, 'day')

        return s2_sr_cld_col_eval.filterDate(start_day, end_day).reduce(ee.Reducer.median())

    images = ee.List(dates_list).map(get_images)
    collection = ee.ImageCollection.fromImages(images)

    return collection


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
        draw.text(copywrite_xy, copywrite, fill="white", font=copywrite_font)
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

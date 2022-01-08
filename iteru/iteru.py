"""The main module for the interactive mapping based on Google Earth Enigne Python API and Ipyleaflet Package """


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
            self.layout.height = '550px'
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
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 0.5
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
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
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 0.1
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
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


def add_DATE_to_imgcol(img):
    return img.set({"DATE": ee.Date(img.get("system:time_start")).format('YYYY-MM-dd')})


def get_imgCol_dates(col):
    col = col.map(add_DATE_to_imgcol)
    return col.aggregate_array('DATE').getInfo()



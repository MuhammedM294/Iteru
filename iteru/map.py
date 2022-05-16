""" The Main Module for The Interactive Mapping Based on Ipyleaflet Package """

import ipywidgets
import ee
import ipyleaflet
from ipywidgets import *
from IPython.display import display
from ipyleaflet import WidgetControl
from .iterugee import *
from .common import *
import geemap


class Map(geemap.Map):
    """
    Inherting the Map class from ipyleaflet with the all its methods and attributes
    """

    def __init__(self, **kwargs):

        Map.zoom_control = False

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

        self.clear_controls()
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

        self.add_control(TOC_widget)

        def add_to_map(change):
            if change.new:
                self.add_layer_widgets(change.new)

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
            if isinstance(object, (ee.Image, ee.ImageCollection, ee.FeatureCollection)):
                layer = ee_tilelayer(object, vis_params)
                if name is None:
                    name = object.getInfo()['id']

            elif isinstance(object, ipyleaflet.TileLayer):
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
            #print('layer already on the map')

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


TOC = ipywidgets.ToggleButton(
    value=False,
    tooltip='Table of Contents',
    icon='archive',
    layout=ipywidgets.Layout(width='32px', height='28px'),
)

TOC_container = ipywidgets.HBox([TOC])
TOC_out = ipywidgets.Output(layout={'border': '1px solid blue'})


def TOC_container_click(change):
    if change.new:
        TOC_container.children = [TOC, TOC_out]
    else:
        TOC_container.children = [TOC]


TOC.observe(TOC_container_click, names='value')

TOC_widget = ipyleaflet.WidgetControl(widget=TOC_container, position='topleft')

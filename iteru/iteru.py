"""Main module."""

import ipyleaflet 
import ee
import os
from ipywidgets import *
from .map_widgets import *
from .common import *
from IPython.display import display

 
class AddWidget(ipyleaflet.WidgetControl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class AddLegend(ipyleaflet.LegendControl ):

    def __init__(self, legend, *args, name="Legend", **kwargs):
        super().__init__(legend, *args, name=name, **kwargs)

class TileLayer(ipyleaflet.TileLayer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SplitMap(ipyleaflet.SplitMapControl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def ee_tilelayer(ee_object, vis_params = None, name ='ee layer'):
        
        ee_object_id =ee_object.getMapId(vis_params)

        ee_object_tile = ipyleaflet.TileLayer(
        
              url = ee_object_id['tile_fetcher'].url_format,
              attribution = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
              name = name, 
              overlay = True,
              control = True
        )
        return ee_object_tile


basemap_tool_widget = AddWidget(widget = basemap_tool, position = 'topleft')
terrain_dataset_tool_widget = AddWidget(widget = terrain_dataset_tool, position = 'topleft')
TOC_widget = AddWidget(widget = TOC_container, position = 'topleft')

class Map(ipyleaflet.Map):
    
    def __init__(self,**kwargs):

        Map.zoom_control = False

        if 'center' not in kwargs:
            kwargs['center'] = [27,31]

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
                 zoom = 10 ,
                 marker = ipyleaflet.Marker(
                                            icon=ipyleaflet.AwesomeIcon(name="check", 
                                            marker_color='green', icon_color='darkgreen')
                                            )
                                  )
                        )
        
        self.add_control(ipyleaflet.ScaleControl(position = 'bottomleft'))

        self.add_control(ipyleaflet.LayersControl(position = 'topleft'))

        self.add_control(ipyleaflet.ZoomControl(position = 'topright'))

        self.add_control(ipyleaflet.FullScreenControl(position = 'topright'))

        draw_control = ipyleaflet.DrawControl(position = 'topright')

        draw_control.polyline =  {
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

        measure = ipyleaflet.MeasureControl( 
                                            position='topright', 
                                            active_color = 'orange',
                                            primary_length_unit = 'kilometers',
                                            secondary_length_unit = ('miles'),
                                            secondary_area_unit = ('acres')
                                           )

        measure.add_area_unit('Sq Kilometers', 1e-6,4)
        measure.primary_area_unit = ('Sq Kilometers')

        self.add_control(measure)  
        self.add_control(basemap_tool_widget)
        self.add_control(terrain_dataset_tool_widget)
        self.add_control(TOC_widget )


    def add_ee_layer(self, ee_object, vis_params=None, name = ''):

        map_id_dict = ee_object.getMapId(vis_params) 
        
        ee_object_tile = ipyleaflet.TileLayer(

            url=map_id_dict['tile_fetcher'].url_format,
            attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
            name=name,
            overlay=True,
            control=True
        )
        self.add_layer(ee_object_tile)

    
        
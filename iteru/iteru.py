"""Main module."""


import ipyleaflet 
import ee
import os
from ipywidgets import *


from .GEEDataset import *
from .basemaps import *
from .common import *
from IPython.display import display


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

        
        basemaps = Dropdown(
                     options = basemaps_dataset,
                     value = None,
                     description = '',
                     description_tooltip = 'Select Basemap',
                     layout=Layout(width='200px'),
                     style = {'description_width': 'initial'}
               )

        terrain = Dropdown(
                     options = terrain_dataset,
                     value = None,
                     description = '',
                     description_tooltip = 'GEE Terrain Dataset',
                     layout=Layout(width='200px'),
                     style = {'description_width': 'initial'}
             )

        basemaps_button = ToggleButton(
                               value = False, 
                               tooltip = 'Basemaps',
                               icon = 'map',
                               layout = Layout(width = '32px', height = '28px'),
        )
        terrain_dataset_button = ToggleButton(
                               value = False, 
                               tooltip = 'GEE Terrain Dataset',
                               icon = 'server',
                               layout = Layout(width = '32px', height = '28px'),
        )
        TOC = ToggleButton(
                               value = False, 
                               tooltip = 'Table of Contents',
                               icon = 'archive',
                               layout = Layout(width = '32px', height = '28px'),
       )


        basemap_tool = HBox([basemaps_button])
        terrain_dataset_tool = HBox([terrain_dataset_button])
        TOC_container = HBox([TOC])
        TOC_out = Output(layout={'border': '1px solid blue'})

        def basemap_tool_click(change):
            if change.new:
                basemap_tool.children = [basemaps_button,basemaps]
            else:
               basemap_tool.children = [basemaps_button]
          
        def terrain_tool_click(change):
            if change.new:
                terrain_dataset_tool.children = [terrain_dataset_button, terrain]
            else:
                terrain_dataset_tool.children = [terrain_dataset_button] 
        
        def TOC_container_click(change):
            if change.new:
                TOC_container.children = [TOC,TOC_out]
            else:
                TOC_container.children = [TOC]     

        basemaps_button.observe(basemap_tool_click, names = 'value')
        terrain_dataset_button.observe(terrain_tool_click, names = 'value')
        TOC.observe(TOC_container_click, names = 'value') 

        basemap_tool_widget = ipyleaflet.WidgetControl(widget = basemap_tool, position = 'topleft')
        terrain_dataset_tool_widget = ipyleaflet.WidgetControl(widget = terrain_dataset_tool, position = 'topleft')
        TOC_widget = ipyleaflet.WidgetControl(widget = TOC_container, position = 'topleft') 

        self.add_control(basemap_tool_widget)
        self.add_control(terrain_dataset_tool_widget)
        self.add_control(TOC_widget )

        def layer_widgets(change):
            if change.new:
                if type(change.new) is ee.image.Image:
                    layer = ee_tilelayer(change.new)
                    name = change.new.getInfo()['id']
                
                elif type(change.new) is ipyleaflet.leaflet.TileLayer:
                     layer = change.new
                     name = change.new.name
                
            if layer in self.layers:
                pass
            else:  
                self.add_layer(layer)
            
                close_button = Button(  
                                value = False, 
                                tooltip = 'Remove This Layer',
                                icon = 'window-close',
                                layout = Layout(width = '32px', height = '28px'),   
                )

                layer_visibility = Checkbox(
                               value = True, 
                               indent=False,
                               layout = Layout(width = '15px')
                )
                
                layer_name = Label(
                                   value= name,
                                   layout = Layout(width = '150px', height = '28px'),
                                   tooltip = name
               )
                opacity = FloatSlider(
                                      value = 1,
                                      min = 0,  
                                      max = 1,
                                      step = 0.1,
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
                
            opacity_slider = interactive(change_layer_opacity,Opacity = opacity)
                
            visibility_checkbox = interactive(change_layer_visibility,show_hide = layer_visibility)
                
            with TOC_out:
                
                display(HBox([layer_visibility,layer_name,opacity, close_button]))
                   
            close_button.on_click(remove_layer) 
            
        basemaps.observe(layer_widgets, names = 'value')
     
        terrain.observe(layer_widgets, names= 'value')

    def zoom_to (self,ee_object, zoom = 8):
        
            try:
                lat = ee_object.geometry().centroid().getInfo()['coordinates'][1]
                long = ee_object.geometry().centroid().getInfo()['coordinates'][0]
                self.center = (lat,long)
                self.zoom = zoom
            except:
                self.center = (27,31)
                self.zoom = 5
                print('Error: can not get the centroid of the Object')    
    

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







    
        
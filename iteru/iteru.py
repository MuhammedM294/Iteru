"""Main module."""


import ipyleaflet 
import ee
from ipywidgets import *

from .gui_widgets import *
from .common import *
from IPython.display import display


def ee_tilelayer(ee_object, vis_params = None, name =''):
        
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
        self.last_draw = draw_control.last_draw
        self.last_action = draw_control.last_action

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

        def add_to_map(change):
            if change.new:
                self.add_layer_widgets(change.new)

        basemaps.observe(add_to_map, names = 'value')
        terrain.observe(add_to_map, names = 'value')  

    def add_layer_widgets(self, object, vis_params = None, name =None):
        try:
            if type(object) is ee.image.Image or type(object) is ee.imagecollection.ImageCollection :
                layer = ee_tilelayer(object,vis_params)
                if name is None:
                   name = object.getInfo()['id']
        
            elif type(object) is ipyleaflet.leaflet.TileLayer:
                layer = object
                if name is None:
                   name = object.name
        except:
            print('input layer is not supported ')
     
        try:
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
        
        except Exception:
            pass
            #print(f'layer already on the map: {layer}')
       
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

    



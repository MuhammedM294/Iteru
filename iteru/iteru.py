"""Main module."""
import ipyleaflet 

class Map(ipyleaflet.Map):

    def __init__(self,**kwargs):

        if 'center' not in kwargs:
            kwargs['center'] = [27,31]

        if 'zoom' not in kwargs:
            kwargs['zoom'] = 5

        if 'scroll_wheel_zoom' not in kwargs:
            kwargs['scroll_wheel_zoom'] = True

        super().__init__(**kwargs)

        if 'height' not in kwargs:
            self.layout.height = '550px'
        else:
            self.layout.height = kwargs['height']

        self.add_control(ipyleaflet.ScaleControl(position = 'bottomleft'))
        self.add_control(ipyleaflet.ZoomControl(position = 'topright'))
        self.add_control(ipyleaflet.FullScreenControl(position = 'topright'))
        self.add_control(ipyleaflet.LayersControl(position = 'topleft'))
        self.add_control(ipyleaflet.DrawControl(position = 'topright'))

class Basemap(ipyleaflet.basemaps):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        pass



    

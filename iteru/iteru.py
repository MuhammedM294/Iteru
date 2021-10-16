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


        self.add_control(ipyleaflet.ScaleControl(position = 'bottomleft'))
        self.add_control(ipyleaflet.ZoomControl(position = 'topright'))
        self.add_control(ipyleaflet.FullScreenControl(position = 'topright'))
        self.add_control(ipyleaflet.LayersControl(position = 'topleft'))

        


    

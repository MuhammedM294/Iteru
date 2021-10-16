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


    

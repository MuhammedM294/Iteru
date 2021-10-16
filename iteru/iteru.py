"""Main module."""
import ipyleaflet 

class Map(ipyleaflet.Map):

    def __init__(self,**kwargs):

        if 'center' not in kwargs:
            kwargs['center'] = [45,45]

        if 'zoom' not in kwargs:
            kwargs['zoom'] = 5


        super().__init__(**kwargs)


    

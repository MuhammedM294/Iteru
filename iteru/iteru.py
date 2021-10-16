"""Main module."""
import ipyleaflet 

class Map(ipyleaflet.Map):

    def __init__(self,**kwargs):

        super().__init__(**kwargs)


    

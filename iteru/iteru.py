"""Main module."""
import ipyleaflet


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

        self.add_control(ipyleaflet.ScaleControl(position = 'bottomleft'))

        self.add_control(ipyleaflet.ZoomControl(position = 'topright'))

        self.add_control(ipyleaflet.FullScreenControl(position = 'topright'))

        self.add_control(ipyleaflet.LayersControl(position = 'topleft'))

        self.add_control(ipyleaflet.DrawControl(position = 'topright'))

        self.add_control(ipyleaflet.SearchControl(position="topleft",
                         url='https://nominatim.openstreetmap.org/search?format=json&q={s}',
                         zoom = 10 ,
                         marker = ipyleaflet.Marker(icon=ipyleaflet.AwesomeIcon(name="check", marker_color='green', icon_color='darkgreen'))
                         ))

    def add_basemap(self, basemap):
        
        if basemap == 'Google_Map':

            basemap = ipyleaflet.TileLayer(
                url = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                attribution='Google',
                name='Google Map'
            )
            self.add_layer(basemap)

        elif basemap == 'Google_Satellite':

            basemap = ipyleaflet.TileLayer(
              url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
              attribution="Google",
              name="Google Satellite",
            )
            self.add_layer(basemap)
        
        return Map



    

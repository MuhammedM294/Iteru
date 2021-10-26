from ipywidgets import *

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
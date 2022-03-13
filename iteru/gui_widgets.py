from .basemaps import basemaps_dataset
from .GEEDataset import terrain_dataset
from ipywidgets import *
from ipyleaflet import WidgetControl


basemaps = Dropdown(
    options=basemaps_dataset,
    value=None,
    description='',
    description_tooltip='Select Basemap',
    layout=Layout(width='200px'),
    style={'description_width': 'initial'}
)
terrain = Dropdown(
    options=terrain_dataset,
    value=None,
    description='',
    description_tooltip='GEE Terrain Dataset',
    layout=Layout(width='200px'),
    style={'description_width': 'initial'}
)
basemaps_button = ToggleButton(
    value=False,
    tooltip='Basemaps',
    icon='map',
    layout=Layout(width='32px', height='28px'),
)
terrain_dataset_button = ToggleButton(
    value=False,
    tooltip='GEE Terrain Dataset',
    icon='server',
    layout=Layout(width='32px', height='28px'),
)
TOC = ToggleButton(
    value=False,
    tooltip='Table of Contents',
    icon='archive',
    layout=Layout(width='32px', height='28px'),
)

basemap_tool = HBox([basemaps_button])
terrain_dataset_tool = HBox([terrain_dataset_button])
TOC_container = HBox([TOC])
TOC_out = Output(layout={'border': '1px solid blue'})


def basemap_tool_click(change):
    if change.new:
        basemap_tool.children = [basemaps_button, basemaps]
    else:
        basemap_tool.children = [basemaps_button]


def terrain_tool_click(change):
    if change.new:
        terrain_dataset_tool.children = [terrain_dataset_button, terrain]
    else:
        terrain_dataset_tool.children = [terrain_dataset_button]


def TOC_container_click(change):
    if change.new:
        TOC_container.children = [TOC, TOC_out]
    else:
        TOC_container.children = [TOC]


basemaps_button.observe(basemap_tool_click, names='value')
terrain_dataset_button.observe(terrain_tool_click, names='value')
TOC.observe(TOC_container_click, names='value')

basemap_tool_widget = WidgetControl(widget=basemap_tool, position='topleft')
terrain_dataset_tool_widget = WidgetControl(
    widget=terrain_dataset_tool, position='topleft')
TOC_widget = WidgetControl(widget=TOC_container, position='topleft')

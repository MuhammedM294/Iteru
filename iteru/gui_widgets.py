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


# first try for the visualiztion parametrs
# image with muliple bands
vis_params = {'bands': ['B5', 'B4', 'B3'],
              'min': None, 'max': None, 'gamma': [0.95, 1.1, 1]}
vis_min = BoundedFloatText(value=0, min=0, max=1000,
                           step=0.1, layout=Layout(width='140px'))
vis_max = BoundedFloatText(value=10, min=0, max=1000,
                           step=0.1, layout=Layout(width='140px'))
vis_gamma_b1 = BoundedFloatText(
    value=None, min=0, max=10, step=0.1, layout=Layout(width='140px'))
vis_gamma_b2 = BoundedFloatText(
    value=None, min=0, max=10, step=0.1, layout=Layout(width='140px'))
vis_gamma_b3 = BoundedFloatText(
    value=None, min=0, max=10, step=0.1, layout=Layout(width='140px'))
band1 = Dropdown(options=['B1', 'B2', 'B3', 'B4', 'B5',
                 'B6', 'B7', 'B8', 'B9'], layout=Layout(width='150px'))
band2 = Dropdown(options=['B1', 'B2', 'B3', 'B4', 'B5',
                 'B6', 'B7', 'B8', 'B9'], layout=Layout(width='150px'))
band3 = Dropdown(options=['B1', 'B2', 'B3', 'B4', 'B5',
                 'B6', 'B7', 'B8', 'B9'], layout=Layout(width='150px'))
apply = Button(description='Apply', button_style='info',
               layout=Layout(width='100px'))


def bands(b1, b2, b3):
    vis_params['bands'][0] = b1
    vis_params['bands'][1] = b2
    vis_params['bands'][2] = b3


def gamma_value(gamma_b1, gamma_b2, gamma_b3):

    vis_params['gamma'][0] = gamma_b1
    vis_params['gamma'][1] = gamma_b2
    vis_params['gamma'][2] = gamma_b3


def min_max_value(min_value, max_value):
    vis_params['min'] = min_value
    vis_params['max'] = max_value


bands_widgets = interactive(bands, b1=band1, b2=band2, b3=band3)
values_widgest = interactive(
    min_max_value, min_value=vis_min, max_value=vis_max)
gamma_w = interactive(gamma_value, gamma_b1=vis_gamma_b1,
                      gamma_b2=vis_gamma_b2, gamma_b3=vis_gamma_b3)
bands_widgets = HBox([band1, band2, band3])
gamma_widgets = HBox([vis_gamma_b1, vis_gamma_b2, vis_gamma_b3])
values_widgets = HBox([vis_min, vis_max])

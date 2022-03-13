from ipywidgets import *
from ipyleaflet import WidgetControl

TOC = ToggleButton(
    value=False,
    tooltip='Table of Contents',
    icon='archive',
    layout=Layout(width='32px', height='28px'),
)

TOC_container = HBox([TOC])
TOC_out = Output(layout={'border': '1px solid blue'})

def TOC_container_click(change):
    if change.new:
        TOC_container.children = [TOC, TOC_out]
    else:
        TOC_container.children = [TOC]



TOC.observe(TOC_container_click, names='value')

TOC_widget = WidgetControl(widget=TOC_container, position='topleft')

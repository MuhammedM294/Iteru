"""A Module with some common functions  """


import os
import ee
from ipywidgets import *
from IPython.display import display
import geemap

geemap.ee_initialize(auth_mode='gcloud')

GERD_aoi = ee.Geometry.Polygon([[
        [
            35.008243,
            10.522199
        ],

        [
            35.008243,
            11.266588
        ],

        [
            35.387092,
            11.266588
        ],

        [
            35.387092,
            10.522199
        ],

        [
            35.008243,
            10.522199
        ]
    ]
]
)

GERD_aoi_dam = ee.Geometry.Polygon([
    [
        [
            35.089645,
            11.208124
        ],
        [
            35.008278,
            11.207198
        ],

        [35.007935,
         10.521569
         ],

        [
            35.387306,
            10.522244
        ],

        [
            35.386963,
            11.265959
        ],
        [
            35.11857,
            11.26638
        ],
        [
            35.089645,
            11.208124
        ]
    ]
]

)

GERD_aoi_zoom_14_1 = ee.Geometry.Polygon([
    [
        [
            35.065441,
            11.155077
        ],
        [
            35.065441,
            11.22774
        ],
        [
            35.164661,
            11.22774
        ],
        [
            35.164661,
            11.155077
        ],
        [
            35.065441,
            11.155077
        ]
    ]
]

)

GERD_aoi_zoom_14_2 = ee.Geometry.Polygon(
    [
        [
            [
                35.027504,
                11.133434
            ],
            [
                35.027504,
                11.210565
            ],
            [
                35.119686,
                11.210565],
            [
                35.119686,
                11.133434
            ],
            [
                35.027504,
                11.133434
            ]
        ]
    ]

)
GERD_aoi_zoom_14_3 = ee.Geometry.Polygon([
    [
        [
            35.065269,
            11.072793
        ],
        [
            35.065269,
            11.155161
        ],
        [
            35.164833,
            11.155161
        ],
        [
            35.164833,
            11.072793
        ],
        [
            35.065269,
            11.072793
        ]
    ]
])

GERD_aoi_zoom_14_4 = ee.Geometry.Polygon([
    [
        [
            35.164833,
            11.072961
        ],
        [
            35.164833,
            11.183791
        ],
        [
            35.248432,
            11.183791
        ],
        [
            35.248432,
            11.072961
        ],
        [
            35.164833,
            11.072961
        ]
    ]
]

)
GERD_aoi_zoom_14_5 = ee.Geometry.Polygon([
    [
        [
            35.131016,
            10.965966
        ],
        [
            35.131016,
            11.072119
        ],
        [
            35.247059,
            11.072119
        ],
        [
            35.247059,
            10.965966
        ],
        [
            35.131016,
            10.965966
        ]
    ]
]
)

GERD_aoi_zoom_14_6 = ee.Geometry.Polygon([
    [
        [
            35.108528,
            10.541484
        ],
        [
            35.108528,
            10.703792
        ],
        [
            35.238647,
            10.703792
        ],
        [
            35.238647,
            10.541484
        ],
        [
            35.108528,
            10.541484
        ]
    ]
])

GERD_aoi_zoom_14_7 = ee.Geometry.Polygon([
    [
        [
            35.151443,
            10.842748
        ],
        [
            35.151443,
            10.985683
        ],
        [
            35.296326,
            10.985683
        ],
        [
            35.296326,
            10.842748
        ],
        [
            35.151443,
            10.842748
        ]
    ]
])

GERD_aoi_zoom_14_8 = ee.Geometry.Polygon([
    [
        [
            35.149727,
            10.701768
        ],
        [
            35.149727,
            10.843422
        ],
        [
            35.239677,
            10.843422
        ],
        [
            35.239677,
            10.701768
        ],
        [
            35.149727,
            10.701768
        ]
    ]
])

GERD_aoi_zoom_14_9 = ee.Geometry.Polygon([
    [
        [
            35.108528,
            10.541484
        ],
        [
            35.108528,
            10.703792
        ],
        [
            35.238647,
            10.703792
        ],
        [
            35.238647,
            10.541484
        ],
        [
            35.108528,
            10.541484
        ]
    ]
]
)

aois = {'zoom_11': GERD_aoi_dam,
        'zoom_14_1': GERD_aoi_zoom_14_1,
        'zoom_14_2': GERD_aoi_zoom_14_2,
        'zoom_14_3': GERD_aoi_zoom_14_3,
        'zoom_14_4': GERD_aoi_zoom_14_4,
        'zoom_14_5': GERD_aoi_zoom_14_5,
        'zoom_14_6': GERD_aoi_zoom_14_6,
        'zoom_14_7': GERD_aoi_zoom_14_7,
        'zoom_14_8': GERD_aoi_zoom_14_8,
        'zoom_14_9': GERD_aoi_zoom_14_9,

        }

elevation_dataset = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2')\
    .filter(ee.Filter.bounds(GERD_aoi))\
    .select('DSM')\
    .median()\
    .clip(GERD_aoi)\
    .reproject(crs='EPSG:32636', scale=30)

fabdem = ee.ImageCollection("projects/sat-io/open-datasets/FABDEM").median()


def random_string(string_length=3):
    import random
    import string
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(string_length))


def get_gif(url):

    import requests
    import tempfile
    r = requests.get(url, stream=True)
    filename = "TimeSeries_" + random_string() + ".gif"
    out_gif = os.path.join(tempfile.gettempdir(), filename)
    with open(out_gif, 'wb') as file:
        for chunk in r.iter_content(chunk_size=1024):
            file.write(chunk)

    return out_gif


def add_text_to_gif(out_gif, dates_list,
                    dates_font_size=22,
                    copywrite_font_size=15,
                    dates_font_color='black',
                    copywrite_font_color='black',
                    framesPerSecond=3,
                    zoom_level='Zoom Level: 14',
                    zoom_level_font_size=15):

    from PIL import Image, ImageDraw, ImageFont, ImageSequence
    import io
    import pkg_resources

    pkg_dir = os.path.dirname(
        pkg_resources.resource_filename("geemap", "geemap.py"))
    default_font = os.path.join(pkg_dir, "data/fonts/arial.ttf")

    gif = Image.open(out_gif)
    count = gif.n_frames

    width, height = gif.size
    dates_text_xy = (int(0.01 * width), int(0.003 * height))
    copywrite_xy = (int(0.01 * width), int(0.97 * height))
    zoom_level_xy = (int(0.02 * width), int(0.94 * height))

    dates_text = dates_list
    copywrite = '©2022, IteruApp'
    dates_text_font = ImageFont.truetype(default_font, dates_font_size)
    copywrite_font = ImageFont.truetype(default_font, copywrite_font_size)
    zoom_level_font = ImageFont.truetype(default_font, zoom_level_font_size)
    frames = []

    for index, frame in enumerate(ImageSequence.Iterator(gif)):
        frame = frame.convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text(dates_text_xy, dates_text[index],
                  fill=dates_font_color, font=dates_text_font)
        draw.text(copywrite_xy, copywrite,
                  fill=copywrite_font_color, font=copywrite_font)
        draw.text(zoom_level_xy, zoom_level,
                  fill=copywrite_font_color, font=zoom_level_font)

        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        frames.append(frame)

    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000/framesPerSecond),
        loop=0,
        optimize=True,
    )
    return out_gif


def display_gif(out_gif):

    from ipywidgets import Image

    out = Output()
    out.clear_output(wait=True)
    display(out)
    with out:
        with open(out_gif, 'rb') as file:
            image = file.read()
        display(Image(value=image))


def show_plot(x, y,
              x_label, y_label,
              xlabel_fontsize=15,
              ylabel_fontsize=18,
              xticks_rotation=90,
              figwitdth=10,
              figheight=7,
              style='fivethirtyeight',
              grid_status=True,
              legend_label=None
              ):

    import matplotlib.pyplot as plt
    plt.style.use(style)
    f = plt.figure()
    f.set_figwidth(figwitdth)
    f.set_figheight(figheight)
    plt.xlabel(x_label, fontsize=xlabel_fontsize)
    plt.ylabel(y_label, fontsize=ylabel_fontsize)
    plt.grid(grid_status)
    plt.xticks(rotation=xticks_rotation)
    plt.plot(x, y, label=legend_label)
    plt.legend()
    plt.gcf().set_size_inches(18.5, 10.5)


obvserved_area_54 = [45.28, 175.98, 201.38, 212.21, 220.34, 216.43, 208.52, 205.37, 192.17, 189.41,
                     186.22, 181.7, 176.32, 176.1, 173.82, 173.95, 176.4, 172.54, 173.42, 173.45,
                     175, 177.35, 174.78, 158.54, 151.32, 179.13, 171.76, 173.98, 175.26, 194.59,
                     256.74, 343.58, 366.3, 363.82, 359.97, 366.35, 360.46, 358.97, 354.21, 338.37,
                     329.23, 325.84, 322.84, 324.67, 322.76, 318.08, 324.26, 329.6, 318.06, 313.61,
                     287.83, 272.55, 260.88, 267.04]


observed_volume_54 = [0.68, 3.78, 4.55, 4.84, 5.07, 5.05, 4.85, 4.59, 4.24, 4.15, 4.14, 4.17, 3.96, 3.96,
                      3.95, 3.78, 3.79, 3.77, 3.66, 3.77, 3.69, 3.85, 3.82, 3.22, 3.69, 4.23, 3.81, 4.09,
                      3.88, 4.26, 5.98, 8.91, 9.8, 9.69, 9.45, 9.65, 9.46, 9.43, 9.16, 8.92, 8.58, 8.56, 8.36,
                      8.38, 8.25, 7.99, 8.21, 8.74, 8, 7.79, 6.91, 6.47, 6.28, 7.3]


def poly_expected_value(x, y, in_value):

    import numpy
    mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

    predicted_value = mymodel(in_value)

    return predicted_value

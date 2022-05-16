"""A Module with some common functions  """


import os
import ee
from ipywidgets import *
from IPython.display import display


def ee_initialize(token_name="EARTHENGINE_TOKEN"):
    """Authenticates Earth Engine and initialize an Earth Engine session"""
    if ee.data._credentials is None:
        try:
            ee_token = os.environ.get(token_name)
            if ee_token is not None:
                credential_file_path = os.path.expanduser(
                    "~/.config/earthengine/")
                if not os.path.exists(credential_file_path):
                    credential = '{"refresh_token":"%s"}' % ee_token
                    os.makedirs(credential_file_path, exist_ok=True)
                    with open(credential_file_path + "credentials", "w") as file:
                        file.write(credential)

            ee.Initialize()
        except Exception:
            ee.Authenticate()
            ee.Initialize()


ee_initialize(token_name="EARTHENGINE_TOKEN")

GERD_aoi = ee.Geometry.Polygon([[[
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
]]])

GERD_aoi_dam = ee.Geometry.Polygon(
    [
        [
            [
                35.089645,
                11.208124
            ],
            [
                35.008278,
                11.207198
            ],
            [
                35.007935,
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
                    dates_font_size=25,
                    copywrite_font_size=15,
                    dates_font_color='red',
                    copywrite_font_color='black',
                    framesPerSecond=4):

    from PIL import Image, ImageDraw, ImageFont, ImageSequence
    import io
    import pkg_resources

    pkg_dir = os.path.dirname(
        pkg_resources.resource_filename("geemap", "geemap.py"))
    default_font = os.path.join(pkg_dir, "data/fonts/arial.ttf")

    gif = Image.open(out_gif)
    count = gif.n_frames

    width, height = gif.size
    dates_text_xy = (int(0.001 * width), int(0.001 * height))
    copywrite_xy = (int(0.001 * width), int(0.98 * height))

    dates_text = dates_list
    copywrite = '©Iteru, 2022'
    dates_text_font = ImageFont.truetype(default_font, dates_font_size)
    copywrite_font = ImageFont.truetype(default_font, copywrite_font_size)

    frames = []

    for index, frame in enumerate(ImageSequence.Iterator(gif)):
        frame = frame.convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text(dates_text_xy, dates_text[index],
                  fill=dates_font_color, font=dates_text_font)
        draw.text(copywrite_xy, copywrite,
                  fill=copywrite_font_color, font=copywrite_font)
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

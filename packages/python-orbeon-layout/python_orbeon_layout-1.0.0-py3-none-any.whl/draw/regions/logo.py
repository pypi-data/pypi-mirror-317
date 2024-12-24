import base64
from io import BytesIO
from PIL import Image
from ..utils import (SCALE, write_draw_rectangle)


def logo(image, context):
    logo_base64 = context['logo_base64']
    coordinate = {
        'width': 35,
        'height': 29,
        'offset_left': 59,
        'offset_top': 0,
        'left': 0,
        'top': 0,
    }
    write_draw_rectangle(image, coordinate)
    logo_insert(image, coordinate, logo_base64)


def logo_insert(image, coordinate, logo_base64):
    logo_image = get_logo_image(logo_base64, coordinate['width'])
    box = get_center_middle_image_box(logo_image, coordinate)
    box = get_center_middle_image_box(logo_image, coordinate)
    image.paste(logo_image, box)


def get_logo_image(logo_base64, width):
    width = width - 8
    logo_base64_bytes = base64.b64decode(logo_base64)
    logo_image = Image.open(BytesIO(logo_base64_bytes))
    logo_width, logo_height = logo_image.size
    logo_ratio = logo_width / logo_height
    logo_width_new = width * SCALE
    logo_height_new = round(logo_width_new / logo_ratio)
    new_size = (logo_width_new, logo_height_new)
    logo_image = logo_image.resize(new_size, Image.LANCZOS)
    return logo_image


def get_center_middle_image_box(image, coordinate):
    width = coordinate['width']
    height = coordinate['height']
    top = coordinate['top']
    left = coordinate['left']
    offset_left = coordinate.get('offset_left', 0)
    offset_top = coordinate.get('offset_top', 0)
    image_width, image_height = image.size
    image_width /= SCALE
    image_height /= SCALE
    image_margin_center = (width - image_width) / 2
    image_margin_middle = (height - image_height) / 2
    box_left = round((image_margin_center + offset_left + left) * SCALE)
    box_top = round((image_margin_middle + offset_top + top) * SCALE)
    box = (box_left, box_top)
    return box

import base64

from io import BytesIO
import datetime


def convert(image):
    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    filename = get_image_name()
    file_io_values =  byte_io.getvalue()
    filename = filename + '.png'
    file_data = encode_file_to_base64(file_io_values)
    return filename, file_data


def encode_file_to_base64(file_data):
    file_base64_string = None
    if file_data:
        file_data_io = BytesIO(file_data)
        file_base64_string = base64.b64encode(file_data_io.getvalue()).decode()
    return file_base64_string


def get_image_name():
    now_format = '%Y_%m_%d_%H%M%S_%f'
    now = datetime.datetime.now()
    now_string = now.strftime(now_format)
    layout_file_name = '{}_{}'.format('layout', now_string)
    return layout_file_name

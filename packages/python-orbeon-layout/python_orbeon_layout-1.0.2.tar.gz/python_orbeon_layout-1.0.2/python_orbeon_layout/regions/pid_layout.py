from ..utils import write_draw_rectangle, write_text_center


def pid(image, context):

    # TITLE
    coordinate = {
        'width': 28,
        'height': 10,
        'offset_left': 0,
        'offset_top': 0,
        'left': 0,
        'top': 0,
    }
    write_draw_rectangle(image, coordinate)
    pid_title_text = 'PEDIDO'
    pid_title_font = 'MYRIADPRO-BOLD.OTF'
    pid_title_font_fill = '#000'
    pid_title_font_size = 18
    write_text_center(image, coordinate, pid_title_text, pid_title_font, pid_title_font_fill, pid_title_font_size)

    # VALUE
    coordinate = {
        'width': 28,
        'height': 10,
        'offset_left': 0,
        'offset_top': 0 + 10 - 1,
        'left': 0,
        'top': 0,
    }
    write_draw_rectangle(image, coordinate)
    pid_value_text = context['pid']
    pid_value_font = 'MYRIADPRO-BOLD.OTF'
    pid_value_font_fill = '#000'
    pid_value_font_size = 18
    write_text_center(image, coordinate, pid_value_text, pid_value_font, pid_value_font_fill, pid_value_font_size)


def layout(image, context):

    # TITLE
    coordinate = {
        'width': 27,
        'height': 10,
        'offset_left': 3 + 27,
        'offset_top': 0,
        'left': 0,
        'top': 0,
    }
    write_draw_rectangle(image, coordinate)
    layout_title_text = 'LAYOUT'
    layout_title_font = 'MYRIADPRO-BOLD.OTF'
    layout_title_font_fill = '#000'
    layout_title_font_size = 18
    write_text_center(image, coordinate, layout_title_text, layout_title_font, layout_title_font_fill, layout_title_font_size)

    # VALUE
    coordinate = {
        'width': 27,
        'height': 10,
        'offset_left': 3 + 27,
        'offset_top': 0 + 10 - 1,
        'left': 0,
        'top': 0,
    }
    write_draw_rectangle(image, coordinate)
    layout_value_text = context['layout']
    layout_value_font = 'MYRIADPRO-BOLD.OTF'
    layout_value_font_fill = '#000'
    layout_value_font_size = 18
    write_text_center(image, coordinate, layout_value_text, layout_value_font, layout_value_font_fill, layout_value_font_size)
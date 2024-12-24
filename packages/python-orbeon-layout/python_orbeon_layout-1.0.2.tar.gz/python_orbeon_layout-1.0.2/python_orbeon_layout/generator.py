from python_orbeon_layout.main import draw


def generator(data):
    result = {
        'success': False,
        'filename': None,
        'file_data': None,
        'error': None,
    }
    try:
        result = draw(data)
    except Exception as e:
        result['error'] = str(e)
    return result

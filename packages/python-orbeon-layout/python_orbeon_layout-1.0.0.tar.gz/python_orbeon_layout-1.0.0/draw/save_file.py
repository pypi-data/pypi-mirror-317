import base64
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def save_file(result, save_file):
    if save_file:
        if result['success']:
            generated_files_saved_path = BASE_DIR / 'generated_files_saved'
            generated_files_saved_path.mkdir(parents=True, exist_ok=True)
            file_path = generated_files_saved_path / result['filename']
            with open(file_path, "wb") as image_file:
                image_file.write(base64.b64decode(result['file_data']))


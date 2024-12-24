
import unittest

from pathlib import Path
from draw.main import draw
from draw.example_data import get_example_data

BASE_DIR = Path(__file__).resolve().parent.parent


class TestDraw(unittest.TestCase):

    def test_data(self):
        data = get_example_data()
        self.assertIn('pid', data)
        self.assertIn('responsavel_nome', data)
        self.assertIn('responsavel_contato', data)
        self.assertIn('data_inicio', data)
        self.assertIn('data_conclusao', data)

    def test_draw(self):
        result = draw(get_example_data())
        self.assertEqual(result['success'], True)
        self.assertGreater(len(result['filename']), 10)
        self.assertEqual(result['error'], None)
        self.assertGreater(len(result['file_data']), 10000)

    def test_draw_save(self):
        result = draw(get_example_data(), True)
        generated_files_saved_path = BASE_DIR / 'generated_files_saved' / result['filename']
        empty = True
        if generated_files_saved_path.exists():
            if generated_files_saved_path.stat().st_size > 500:
                empty = False
        self.assertFalse(empty)

if __name__ == "__main__":
    unittest.main()

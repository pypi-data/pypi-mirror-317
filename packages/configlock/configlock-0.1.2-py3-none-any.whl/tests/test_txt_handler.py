import unittest
from cryptoconfig.formats import txt_handler

class TestTxtHandler(unittest.TestCase):
    def setUp(self):
        self.sample_text = "This is a test."

    def test_load(self):
        loaded_data = txt_handler.load(self.sample_text)
        self.assertEqual(loaded_data, self.sample_text)

    def test_dump(self):
        dumped_data = txt_handler.dump(self.sample_text)
        self.assertEqual(dumped_data, self.sample_text)

if __name__ == "__main__":
    unittest.main()

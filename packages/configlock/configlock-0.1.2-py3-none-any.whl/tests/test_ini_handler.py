import unittest
from cryptoconfig.formats import ini_handler

class TestIniHandler(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "Section": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        self.ini_content = "[Section]\nkey1 = value1\nkey2 = value2\n"

    def test_load(self):
        parsed_data = ini_handler.load(self.ini_content)
        self.assertEqual(parsed_data, self.sample_data)

    def test_dump(self):
        dumped_data = ini_handler.dump(self.sample_data)
        self.assertEqual(dumped_data.strip(), self.ini_content.strip())

if __name__ == "__main__":
    unittest.main()

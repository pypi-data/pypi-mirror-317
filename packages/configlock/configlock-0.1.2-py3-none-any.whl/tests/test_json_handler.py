import unittest
from cryptoconfig.formats import json_handler

class TestJsonHandler(unittest.TestCase):
    def setUp(self):
        self.sample_data = {"key1": "value1", "key2": "value2"}
        self.json_content = '{\n    "key1": "value1",\n    "key2": "value2"\n}'

    def test_load(self):
        parsed_data = json_handler.load(self.json_content)
        self.assertEqual(parsed_data, self.sample_data)

    def test_dump(self):
        dumped_data = json_handler.dump(self.sample_data)
        self.assertEqual(dumped_data.strip(), self.json_content.strip())

if __name__ == "__main__":
    unittest.main()

import unittest
from cryptoconfig.formats import properties_handler

class TestPropertiesHandler(unittest.TestCase):
    def setUp(self):
        self.sample_data = {"key1": "value1", "key2": "value2"}
        self.properties_content = "key1=value1\nkey2=value2\n"

    def test_load(self):
        parsed_data = properties_handler.load(self.properties_content)
        self.assertEqual(parsed_data, self.sample_data)

    def test_dump(self):
        dumped_data = properties_handler.dump(self.sample_data)
        self.assertEqual(dumped_data.strip(), self.properties_content.strip())

if __name__ == "__main__":
    unittest.main()

import os
import unittest
from cryptoconfig import EncryptedConfigManager

class TestEncryptedConfigManager(unittest.TestCase):
    def setUp(self):
        self.manager = EncryptedConfigManager()
        self.sample_data = {
            "Section": {
                "key1": "value1",
                "key2": "value2"
            }
        }

    def tearDown(self):
        for file in ["test.ini", "test.json", "test.yaml", "test.txt", "test.properties"]:
            if os.path.exists(file):
                os.remove(file)

    def test_save_and_load_ini(self):
        self.manager.save("test.ini", self.sample_data)
        loaded_data = self.manager.load("test.ini")
        self.assertEqual(self.sample_data, loaded_data)

    def test_save_and_load_json(self):
        self.manager.save("test.json", self.sample_data)
        loaded_data = self.manager.load("test.json")
        self.assertEqual(self.sample_data, loaded_data)

    def test_save_and_load_yaml(self):
        self.manager.save("test.yaml", self.sample_data)
        loaded_data = self.manager.load("test.yaml")
        self.assertEqual(self.sample_data, loaded_data)

    def test_save_and_load_txt(self):
        text_data = "This is a test."
        self.manager.save("test.txt", text_data)
        loaded_data = self.manager.load("test.txt")
        self.assertEqual(text_data, loaded_data)

    def test_save_and_load_properties(self):
        self.manager.save("test.properties", self.sample_data)
        loaded_data = self.manager.load("test.properties")
        self.assertEqual(self.sample_data, loaded_data)

if __name__ == "__main__":
    unittest.main()

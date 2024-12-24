import os
import unittest
from cryptoconfig.encryptor import ConfigEncryptor

class TestConfigEncryptor(unittest.TestCase):
    def setUp(self):
        self.key_file = "test_key.key"
        self.encryptor = ConfigEncryptor()
        self.sample_content = "This is a test."

    def tearDown(self):
        if os.path.exists(self.key_file):
            os.remove(self.key_file)
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")

    def test_encrypt_and_decrypt(self):
        self.encryptor.encrypt("test_file.txt", self.sample_content)
        decrypted_content = self.encryptor.decrypt("test_file.txt")
        self.assertEqual(self.sample_content, decrypted_content)

    def test_save_and_load_key(self):
        encryptor_with_key_file = ConfigEncryptor(key_file=self.key_file)
        self.assertTrue(os.path.exists(self.key_file))
        loaded_encryptor = ConfigEncryptor(key_file=self.key_file)
        self.assertEqual(encryptor_with_key_file.key, loaded_encryptor.key)

if __name__ == "__main__":
    unittest.main()

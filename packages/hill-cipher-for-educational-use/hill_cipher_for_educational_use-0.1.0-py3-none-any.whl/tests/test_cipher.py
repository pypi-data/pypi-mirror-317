import unittest
import numpy as np
from hillcipher.cipher import HillCipher

class TestHillCipher(unittest.TestCase):
    def setUp(self):
        """
        Set up a HillCipher instance for testing.
        """
        self.cipher = HillCipher(block_size=2)
        self.cipher.generate_key()

    def test_key_generation(self):
        """
        Test that the generated key is a valid invertible matrix.
        """
        key = self.cipher.key
        self.assertIsNotNone(key, "Key should not be None")
        self.assertEqual(key.shape, (2, 2), "Key should be a 2x2 matrix")
        self.assertTrue(HillCipher._is_invertible(key), "Key should be invertible")

    def test_encryption_and_decryption(self):
        """
        Test that encryption followed by decryption returns the original text.
        """
        plaintext = "HELLO"
        ciphertext = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(ciphertext)
        self.assertEqual(decrypted.strip('X'), plaintext, "Decrypted text should match the original plaintext")

    def test_manual_key_set(self):
        """
        Test setting a manual key and using it for encryption and decryption.
        """
        key = np.array([[3, 3], [2, 5]])
        self.cipher.set_key(key)
        plaintext = "TEST"
        ciphertext = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(ciphertext)
        self.assertEqual(decrypted.strip('X'), plaintext, "Decrypted text should match the original plaintext")

    def test_invalid_key_set(self):
        """
        Test that setting an invalid key raises an error.
        """
        invalid_key = np.array([[1, 2], [3, 6]])  # Non-invertible matrix
        with self.assertRaises(ValueError):
            self.cipher.set_key(invalid_key)

    def test_invalid_text_encryption(self):
        """
        Test that encrypting non-alphabetic text raises an error.
        """
        invalid_text = "12345"
        with self.assertRaises(ValueError):
            self.cipher.encrypt(invalid_text)

    def test_explain_encryption(self):
        """
        Test the explain_encryption method to ensure it runs without errors and produces a valid ciphertext.
        """
        plaintext = "HELLO"
        print("\nRunning explain_encryption test...")
        ciphertext = self.cipher.explain_encryption(plaintext)
        self.assertIsInstance(ciphertext, str, "Ciphertext should be a string.")
        self.assertGreater(len(ciphertext), 0, "Ciphertext should not be empty.")

    def test_explain_decryption(self):
        """
        Test the explain_decryption method to ensure it runs without errors and produces a valid plaintext.
        """
        plaintext = "HELLO"
        ciphertext = self.cipher.encrypt(plaintext)
        print("\nRunning explain_decryption test...")
        decrypted = self.cipher.explain_decryption(ciphertext)
        self.assertIsInstance(decrypted, str, "Decrypted text should be a string.")
        self.assertEqual(decrypted.strip('X'), plaintext, "Decrypted text should match the original plaintext.")

if __name__ == '__main__':
    unittest.main()
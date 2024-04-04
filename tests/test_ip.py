"""Tests for IPAdress class"""
import unittest
from classes.ip import IPAddress


class TestIPAdress(unittest.TestCase):
    """
    Tests the IPAdress class and it's methods
    """

    def test_is_valid(self):
        """Tests if is_valid indeed detects valid and invalid ip adresses"""
        # Testing valid ip adressses
        self.assertTrue(IPAddress("192.168.1.1").is_valid())
        self.assertTrue(IPAddress("10.0.0.1").is_valid())

        # Testing invalid ip adresses
        self.assertFalse(IPAddress("256.256.256.256").is_valid())
        self.assertFalse(IPAddress("192.168.1").is_valid())
        self.assertFalse(IPAddress("test mc testface").is_valid())

    def test_get_octets(self):
        """Tests if get_octets properly separates the ip into its octets"""
        # Test with a valid ip adress
        self.assertEqual(IPAddress("192.168.1.1").get_octets(), [192, 168, 1, 1])

        # Test with an invalid ip adress
        self.assertIsNone(IPAddress("test mc_testface").get_octets())

    def test_str_representation(self):
        """Tests if IPAdress is a string or something"""
        # Test string representation
        ip = IPAddress("192.168.1.1")
        self.assertEqual(str(ip), "192.168.1.1")


if __name__ == "__main__":
    unittest.main()

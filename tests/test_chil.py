"""
Unit tests for the `chilio` module functions.

These tests verify the functionality of:

* `create_toml_file`: Creating new TOML files with basic structure and data.
* `add_entry`: Adding and modifying entries in existing TOML files.

The tests utilize temporary files for isolation and ensure proper cleanup after execution.
"""

import unittest
import os
from tempfile import NamedTemporaryFile
import sys
import toml

sys.path.append("../source")  #! scuffed solution
import apps.chil.lib.ip_list as chilio


class TestChilio(unittest.TestCase):
    """
    Unit test class for the `chilio` module functions.

    Contains tests that verify the functionality of various functions in the `chilio` module,
    specifically focusing on:

    * Creating new TOML files with the basic structure for IP addresses (`create_toml_file`).
    * Adding and modifying entries in existing TOML files (`add_entry`).

    The tests utilize temporary files for isolation and ensure proper cleanup after execution.
    """

    def setUp(self):
        """
        Creates a temporary file for testing purposes.
        """
        with NamedTemporaryFile(delete=False, suffix=".toml") as self.temp_file:
            self.temp_file_name = self.temp_file.name

    def tearDown(self):
        """
        Cleans up by removing the temporary file.
        """
        os.remove(self.temp_file_name)

    def test_create_toml_file(self):
        """
        Tests successful creation of a TOML file with basic structure.
        """
        data = {
            "address": "192.168.0.1",
            "name": "Testland server",
            "description": "This is a test",
        }
        self.assertTrue(chilio.create_toml_file(self.temp_file_name, [data]))

        # Verify file content
        with open(self.temp_file_name, "r", encoding="utf-8") as file:
            content = file.read()
            expected_content = """[ip_addresses]\n[[ip_addresses.entry]]\naddress = "192.168.0.1"\nname = "Testland server"\ndescription = "This is a test"\n"""
            self.assertEqual(content, expected_content)

    def test_add_entry(self):
        """
        Tests adding new entries and modifying existing entries.
        """
        # Create initial data
        data = {
            "address": "192.168.0.1",
            "name": "Server 1",
            "description": "Initial entry",
        }
        chilio.create_toml_file(self.temp_file_name, [data])

        # Test modifying existing entry
        data["name"] = "Modified Server 1"
        self.assertTrue(chilio.add_entry(self.temp_file_name, data))

        # Verify modified content
        with open(self.temp_file_name, "r", encoding="utf-8") as file:
            content = file.read()
            expected_content = """[ip_addresses]\n[[ip_addresses.entry]]\naddress = "192.168.0.1"\nname = "Modified Server 1"\ndescription = "Initial entry"\n"""
            self.assertEqual(content, expected_content)

        # Test adding a new entry
        data2 = {
            "address": "192.168.0.2",
            "name": "Server 2",
            "description": "New entry",
        }
        self.assertTrue(chilio.add_entry(self.temp_file_name, data2))

        # Verify content with both entries
        with open(self.temp_file_name, "r", encoding="utf-8") as file:
            content = file.read()
            expected_content = """[ip_addresses]\n[[ip_addresses.entry]]\naddress = "192.168.0.1"\nname = "Modified Server 1"\ndescription = "Initial entry"\n\n[[ip_addresses.entry]]\naddress = "192.168.0.2"\nname = "Server 2"\ndescription = "New entry"\n"""
            self.assertEqual(content, expected_content)

    def test_load_toml(self):
        """
        Tests successful loading of a valid TOML file and handling of non-existent files.
        """
        # Create a temporary TOML file with content
        data = {
            "ip_addresses": {
                "entry": [{"address": "10.0.0.1", "name": "Database Server"}]
            }
        }
        with open(self.temp_file_name, "w", encoding="utf-8") as file:
            toml.dump(data, file)

        loaded_data = chilio.load_toml(self.temp_file_name)
        self.assertEqual(loaded_data, data)

        # Test non-existent file
        self.assertIsNone(chilio.load_toml("non_existent_file.toml"))

    def test_remove_entry(self):
        """
        Tests successful removal of entries based on their IP address.
        """
        # Create initial data
        data = [
            {"address": "192.168.0.1", "name": "Server 1"},
            {"address": "10.0.0.2", "name": "Server 2"},
        ]
        chilio.create_toml_file(self.temp_file_name, data)

        # Test removing an existing entry
        entry_to_remove = {"address": "192.168.0.1"}
        self.assertTrue(chilio.remove_entry(self.temp_file_name, entry_to_remove))

        # Verify content with only remaining entry
        with open(self.temp_file_name, "r", encoding="utf-8") as file:
            content = file.read()
            expected_content = """[ip_addresses]\n[[ip_addresses.entry]]\naddress = "10.0.0.2"\nname = "Server 2"\n"""
            self.assertEqual(content, expected_content)

        # Test removing a non-existent entry
        entry_to_remove = {"address": "192.168.0.3"}
        self.assertFalse(chilio.remove_entry(self.temp_file_name, entry_to_remove))


if __name__ == "__main__":
    unittest.main()

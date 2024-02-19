"""
Tests chil app
"""

import unittest
from ip_list import add_entry, load_toml, _build_file_path


class TestAddEntry(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            "ip_addresses": {
                "entry": [
                    {
                        "address": "192.168.1.1",
                        "name": "Server 1",
                        "description": "Main server",
                    },
                    {"address": "192.168.1.2", "name": "Server 2"},
                ]
            }
        }

    def tearDown(self):
        pass

    def test_add_new_entry(self):
        new_entry = {"address": "192.168.1.3", "name": "Server 3"}
        result = add_entry("test_file.toml", new_entry, False, self.test_data.copy())
        self.assertTrue(result)

        self.assertEqual(len(self.test_data["ip_addresses"]["entry"]), 3)
        self.assertIn(new_entry, self.test_data["ip_addresses"]["entry"])

    def test_update_existing_entry(self):
        updated_entry = {
            "address": "192.168.1.2",
            "name": "Updated Server Name",
            "description": "New description",
        }
        result = add_entry(
            "test_file.toml", updated_entry, False, self.test_data.copy()
        )
        self.assertTrue(result)

        self.assertEqual(len(self.test_data["ip_addresses"]["entry"]), 2)
        updated_entry_index = [
            i
            for i, entry in enumerate(self.test_data["ip_addresses"]["entry"])
            if entry["address"] == updated_entry["address"]
        ][0]
        self.assertEqual(
            self.test_data["ip_addresses"]["entry"][updated_entry_index], updated_entry
        )

    def test_handle_missing_file(self):
        result = add_entry("nonexistent_file.toml", {"address": "192.168.1.4"}, False)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()

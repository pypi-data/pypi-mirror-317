import unittest
from typing import List

import pytest

from stefan.utils.gspread.gspread_client import GspreadClient

@pytest.mark.slow
class TestGspreadClient(unittest.TestCase):
    def setUp(self):
        self.client = GspreadClient()
        # Initial test data
        self.initial_data = [
            ["Name", "Age", "City"],
            ["John", "30", "New York"],
            ["Alice", "25", "London"]
        ]
        
    def tearDown(self):
        # Clean up after each test by clearing the sheet
        self.client._clear_and_update_worksheet([])

    def test_update_cell(self):
        # Setup initial state
        self.client._clear_and_update_worksheet(self.initial_data)
        
        # Verify initial state
        sheet_data = self.client.show_all_data()
        self.assertIn("John", sheet_data)
        self.assertIn("30", sheet_data)
        
        # Perform update
        self.client.update_cell(2, "B", "31")
        
        # Verify updated state
        updated_data = self.client.show_all_data()
        self.assertIn("31", updated_data)
        self.assertNotIn("30", updated_data)

    def test_insert_row(self):
        # Setup initial state
        self.client._clear_and_update_worksheet(self.initial_data)
        
        # Verify initial state
        initial_data = self.client.show_all_data()
        self.assertIn("John", initial_data)
        self.assertIn("Alice", initial_data)
        
        # Insert new row
        new_row = ["Bob", "35", "Paris"]
        self.client.insert_row(new_row, 2)
        
        # Verify updated state
        updated_data = self.client.show_all_data()
        self.assertIn("Bob", updated_data)
        self.assertIn("Paris", updated_data)
        # Verify order (Bob should be before Alice)
        bob_pos = updated_data.find("Bob")
        alice_pos = updated_data.find("Alice")
        self.assertLess(bob_pos, alice_pos)

    def test_delete_row(self):
        # Setup initial state
        self.client._clear_and_update_worksheet(self.initial_data)
        
        # Verify initial state
        initial_data = self.client.show_all_data()
        self.assertIn("John", initial_data)
        
        # Delete row
        self.client.delete_row(2)  # Delete John's row
        
        # Verify updated state
        updated_data = self.client.show_all_data()
        self.assertNotIn("John", updated_data)
        self.assertIn("Alice", updated_data)

if __name__ == '__main__':
    unittest.main() 
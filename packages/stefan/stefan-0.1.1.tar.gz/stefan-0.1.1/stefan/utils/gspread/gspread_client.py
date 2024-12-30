from typing import List

import gspread
from gspread.worksheet import Worksheet
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition
from gspread.utils import GridRangeType

from stefan.utils.multiline import multiline

class GspreadClient:

    def show_all_data(self) -> str:
        worksheet = self._load_worksheet()

        # Get all rows and columns from the sheet
        list_of_lists = worksheet.get(return_type=GridRangeType.ListOfLists)
        print(f"Debug - Retrieved data type: {type(list_of_lists)}")
        print(f"Debug - Retrieved data: {list_of_lists}")
        
        # Handle empty sheet case
        if not list_of_lists or not list_of_lists[0]:
            return "Sheet is empty"
        
        # Add column letters as header row
        column_letters = [chr(65 + i) for i in range(len(list_of_lists[0]))]  # A, B, C, etc.
        list_of_lists.insert(0, column_letters)
        
        # Calculate maximum width for each column, including row numbers
        row_num_width = len(str(len(list_of_lists)))
        col_widths = []
        for col_idx in range(len(list_of_lists[0])):
            col_width = max(len(str(row[col_idx])) for row in list_of_lists if len(row) > col_idx)
            col_widths.append(col_width)
        
        # Create formatted output
        output = []
        for row_idx, row in enumerate(list_of_lists):
            # Add row number (empty for header row)
            row_num = '' if row_idx == 0 else str(row_idx)
            formatted_row = [row_num.rjust(row_num_width)]
            
            # Format each cell
            for col_idx, cell in enumerate(row):
                formatted_row.append(str(cell).ljust(col_widths[col_idx]))
            output.append(" | ".join(formatted_row))
        
        # Add separator line after column letters
        separator = "-" * len(output[0])
        output.insert(1, separator)
        
        return "\n".join(output)

    def update_cell(self, row: int, col: str, value: str) -> None:
        """
        Update a single cell value.
        Args:
            row: Row number (1-based)
            col: Column letter (A, B, C, etc.)
            value: New cell value
        """
        worksheet = self._load_worksheet()
        # Convert column letter to number (A=1, B=2, etc.)
        col_num = ord(col.upper()) - ord('A') + 1
        worksheet.update_cell(row, col_num, value)

    def insert_row(self, values: List[str], row_index: int) -> None:
        """
        Insert a new row at specified index and fill it with values.
        Args:
            values: List of values for the new row
            row_index: Row index where to insert (1-based)
        """
        worksheet = self._load_worksheet()
        worksheet.insert_row(values, row_index)

    def delete_row(self, row_index: int) -> None:
        """
        Delete a row at specified index.
        Args:
            row_index: Row index to delete (1-based)
        """
        worksheet = self._load_worksheet()
        worksheet.delete_rows(row_index)

    def _load_worksheet(self) -> Worksheet:
        gc = gspread.service_account_from_dict(_SERVICE_ACCOUNT_MAP)
        spreadsheet = gc.open_by_url(_SHEETS_URL)
        worksheet = spreadsheet.sheet1
        return worksheet

    def _clear_and_update_worksheet(self, values: List[List[str]]) -> None:
        """
        Clears the entire worksheet and updates it with new values.

        Args:
            values: List of lists containing the new values to populate the worksheet with
        """
        worksheet = self._load_worksheet()
        # Clear existing content
        worksheet.clear()
        # Update with new values starting from A1
        worksheet.update(values)

class MockGspreadClient:
    def __init__(self):
        self.operations = []
        self._mock_data = [
            ["Section", "Key", "Value"],
            ["General", "key1", "value1"],
            ["Navigation", "key2", "value2"]
        ]

    def show_all_data(self) -> str:
        self.operations.append(("get_all", {}))
        return "\n".join(["\t".join(row) for row in self._mock_data])

    def update_cell(self, row: int, col: str, value: str) -> None:
        self.operations.append(("update_cell", {"row": row, "col": col, "value": value}))

    def insert_row(self, values: List[str], row_index: int) -> None:
        self.operations.append(("insert_row", {"values": values, "row_index": row_index}))

    def delete_row(self, row_index: int) -> None:
        self.operations.append(("delete_row", {"row_index": row_index}))


_SHEETS_URL = "https://docs.google.com/spreadsheets/d/16v1lH5Yb9XwOxaziHp_e9JcBipIpsmVKV5-BisDaoq0/edit?gid=0#gid=0"
    
_SERVICE_ACCOUNT_MAP = {
  "type": "service_account",
  "project_id": "tempo2runn",
  "private_key_id": "46e411971b40677281594d0f23a388d58dedc494",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCryz0safzhtxPX\nPMj5MuJEtpNJmb8qII5tAkW+M42XqrjVgy2ICylTcQtSIJkHiz+SvSEnYwJaHZ3y\n4Vk8s8QC9GrNN3Nl8wvYv0ZLCQazoAypSXUSEwN4W++otbVdlfWbomycLr8HTSM/\nu+3KIWcHaZbtVi+XZdgNetW03ft3AOYkZ3YCkXBWGEcT3z7idq4eF6+3REopQ0DM\nFaEQXDhpCu/SVd3+o3pQKNdTiyXfJUA9EvFVMZkkZqT9W7pw8Nm3PbeL63Q7mRec\nuPZ7lMLw/ooAslegpEK16qCLqs1o16xvHF4rCneu7wL+fK1HXe6p6pzJa6PKwhfB\ncG6yhEF3AgMBAAECggEAUmod3sC54E7D5e3zPBl9ExnDbvujCcK0kPcWHjj9JFVy\ndnuHzEwOd0kz9SJOR6A1z1+MGCkXZ8PtkicpeEWFMyWuVuTTJ4WBmWmpfzXFUUbm\nzA/BafpVH9h7EKSbbVoTiaZSFFsYqZgH4Pt3CBEeLCArl5BRJIBnNZBIFYyopl2t\nlyloSkfDo+zqns7XrrytSbX9wjh6D0u/EVFzTgHRFV6Dky0wQsVN3lqC9q6mxyG5\nIO8YzWv+uYcOyc8DFccZVzrjJ8LGyUPnsvuhWKIUEZGoO4TLcRBi9HY37lPAh074\n3WWF7T2uXFTJZfWbkNF7ni31JjoC69Zqd2s4X0FUAQKBgQDqTSTJbvaUEZT/xFBt\n1jJSD5iQpkuiZM/Row1aXTvnWt21JOZla8UDRtpnu8PrEv6G94Qoeaivp38XcVil\nJXiZZW5sevwqdm+Oxjomeu01NE9VgDUjDDXT3U44++/8xhS7ynx0TtXPHWyiRc+Q\nd1YUlgOHT2smdsRDm8xBP3srYQKBgQC7tCh+CWCkaaNW2VEkL6rsGBxO8UM0qr0O\nQYVOprU75DrV9RVKEGnb+Ta22KT8m1t8Jhfj2pVzR3FSQzQX/d7J6KOx9zilx65I\nKbeUTLXH8UVWhyhWJPIc/aqBDy27LgjmHrXGAr06RSO/eke+C/vDzXk7F+hxjiaO\nEvcJiX6z1wKBgQChvM8AHhEo9VodlK7Qo2PpMcrnT2Q2ndC3rg6xqlqHwjn5qZdB\nu7ssH+T0ZrE/vMTm9kXMiu7fEoiw7hV7KvqtKU+oot0fktI/hKbvmTvV1l5Nb0s+\n/lbKAaLVw1RO8Y2udICk6Sa+6ljrS7WUzEwnucaFyVT2IFYrNYkyIVgtAQKBgQCL\naBiS0yAlvBeGD00GVSjaxGVx9Bn36b8T8XGyonoEC1PvSGERavNUXtlWH70Zp8Dg\nieJAZj2NKshtUmBEWVa4GsJJENXPumgkTGd+CyMPZpAa3bMFl9cB1RxnUgCi/mO5\nlaFneO1Vc7hDI+xYp8nK+LZLP0xx2iOkbU1wld+2bQKBgQC3RwuXD6cEZVbZGBLJ\nDfHBiGflbm0YDGcbSPJhL6t0y0pyACvukrpCdCq2e3caMNx/2p0Um8o/dZs67NCe\nllFpv2NK1L1Tl+dqb0ByQBp0VF8Oqk8XkKdWKXhM7huXqVPA4kFovOvHYCdEjP8u\nTmAuARQqUwsK8RNem8DnajcUOQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "stefan-the-coder@tempo2runn.iam.gserviceaccount.com",
  "client_id": "101355419010239849674",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/stefan-the-coder%40tempo2runn.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

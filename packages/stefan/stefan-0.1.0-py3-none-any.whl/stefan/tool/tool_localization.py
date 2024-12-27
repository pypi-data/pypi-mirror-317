import inspect
from typing import Dict, Any

import gspread
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition
from gspread.utils import GridRangeType
list_of_lists = worksheet.get(return_type=GridRangeType.ListOfLists)

class AddStringsToolDefinition(ToolDefinition):
    name: str = "add_and_update_strings"
    description: str = "This tool should be used when you need to update strings in the project. Since all string resources are stored in Google Sheets and then updated via script, you should not touch xml strings and instead of you should always update this translation sheet instead. Strings will be updated automatically when this tool finishes."
    parameters: Dict[str, str] = {
        "command": "(required, multiple) The command which will be used to update google sheets."
    }
    usage: str = inspect.cleandoc("""
    <add_and_update_strings>
        <command>
        </command>
    </add_and_update_strings>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        gc = gspread.service_account_from_dict(_SERVICE_ACCOUNT_MAP)
        spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/16v1lH5Yb9XwOxaziHp_e9JcBipIpsmVKV5-BisDaoq0/edit?gid=0#gid=0")
        worksheet = spreadsheet.sheet1
        list_of_lists = worksheet.get(return_type=GridRangeType.ListOfLists)
        
        # Calculate maximum width for each column
        col_widths = []
        for col_idx in range(len(list_of_lists[0])):
            col_width = max(len(str(row[col_idx])) for row in list_of_lists)
            col_widths.append(col_width)
        
        # Create formatted output
        output = []
        for row in list_of_lists:
            formatted_row = []
            for col_idx, cell in enumerate(row):
                formatted_row.append(str(cell).ljust(col_widths[col_idx]))
            output.append(" | ".join(formatted_row))
        
        # Add separator line after header
        separator = "-" * len(output[0])
        output.insert(1, separator)
        
        return "\n".join(output)
    
_SERVICE_ACCOUNT_MAP = {
  "type": "service_account",
  "project_id": "tempo2runn",
  "private_key_id": "b50ea9fd3f381e77e9f63068c9b58749da034afc",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCzRbSy2A6/P9ep\nTW92WgJ8uc7YrcEW0VQeuqhx94Ujqu4GSgGBmQqe2U3dzOguAcHdM63Hn21Y2r1T\n1s7FCg9QrdIfhCgUCremeG1CDKbW13WGVBojphPvzFua9wH0dB0kR+K//3IoBadC\n7YPZQXbhFRpsUaXb67nNzWs+H1hsEtXY1zwsfL2LOoffIJ+RXj+vWCQO0xtyf21C\nfrM981QMsCeEvIQk1KquFS2fGItAiNQEbX3B+bpBLc/EDgTH7xrahi3EvSomKnjn\ntXLo7oQaZjpND7CN+DOO1SZ8bkijx0ASwczSqdPvwaSdzhvvg+S8VxV+BiHDbHXt\n2R8dUrrBAgMBAAECggEABBwKoA2V4PUiCM6D9JmW9Fb/Z+DWdqMbzjcx2f2g6V1n\nZsYsMgADyfpp74tdSINfzKX89iuFwoNZKGKEi5McdhlV92+nH4vTWUHqIe56UJ3Q\neDYrVzqHuyKFzbqbKohoNpxd6qV8xMVvEnixYg8/Hg/GyEmNh3S9kKXZ2dW2yDC9\n0Cz0dsmIPquOsEFUGMUnDLt55lGFQiGFFeUfYgKglVgwidaBv0tWaS1a7sBIXicw\ngZ6unEK01lT1HS/V93xFAb8mSISOzDSYRRvBlDL9RiBxQDv5KUs377SzmtAZ1iuJ\nfvCQya6MUapvCOJkEQO48aCPsEkw0GaJBFJC3X9J9QKBgQDrNb9YOjMMeQ3PifVU\n7KBY7rFN4ijAwBWbGMhRY7JVBqdn6P1rIIVGCEGoanRFPZn5pF+cBSHCokuvBuqy\n2A0RMIb4J2gvlZ9+rI6dhBF793W3lfgtlBDdnDVxAqfir+ZDwTVwC5TJJsGUVtTq\ncAxhFwjESaKWVxWpvtXcr08/OwKBgQDDHjg2601SSxDToP6zMk2Uo3rviuH6MgZw\nn14fqESHv0ylIng5e9xdktaDFf1RA2fz98sLjXmMUWK0gluj2HDdL7xLFcayTEIx\nGBnvs0PRIj/aeGcUHOKGd+H/vWrzy1D/E8uvREUm6/mGmGjfH/bePWNzMoj1ihmN\nYv6gec1GMwKBgGFGeTwj1bjy16Ndivj0Y9xj2zA6uF//EPBz72S5tqczeUigMy56\n5KNyBrWAUVXRhDyannAIL04vkN1yHt6YO89AIpG+unfziWL6OoEqfZCnZyfl/h3b\nfp4oXHHAh25ZEQI0hcUxBPer76NJxgSvEm+U9ys2yOckXPE223vJhRzBAoGAARAY\nFEyB1lHsXIrC+GzsuUOOtuFVy8wb9t8XXyrGfMrQ+xFOAFopYCUdoActoxRWq6CM\n7ZousFH9LKiNIT5blwjciLgspen+blAITCL42pnKKUGApj5mCX97rq30eDGCVnFg\nKatAiS695DrOT3DYImvJL+Z1kojXDMseQfeH47sCgYBL75mQuaZSM2h5kAZXfmW3\nsu7rsRHg3Kf+W8BzVUCIN7jwpNR1fM8DFz4AnIuvHCMzMcv+DM5GSXush7lrUvBb\n15fGCcrO+3A/3n+BlQA1plBF+9C0J1gDHvwhAbZbII5AfKSKtn/s/uNW9J47npRA\n2eGkp5rxwLtySmOeYDc3Ew==\n-----END PRIVATE KEY-----\n",
  "client_email": "stefan-coder-service-account@tempo2runn.iam.gserviceaccount.com",
  "client_id": "108366166351472347375",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/stefan-coder-service-account%40tempo2runn.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

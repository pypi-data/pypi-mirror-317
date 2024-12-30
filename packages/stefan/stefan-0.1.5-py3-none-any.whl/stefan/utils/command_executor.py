import subprocess
from typing import Tuple

class CommandExecutor:
    @staticmethod
    def execute(command: str) -> Tuple[bool, str]:
        """
        Execute a command line command and return the results
        
        Args:
            command: Command to execute as a string
            
        Returns:
            Tuple[bool, str]: A tuple containing:
                - bool: True if command executed successfully, False if failed
                - str: Output message from the command execution
        """
        try:
            # Run the command as a shell command to preserve spacing
            result = subprocess.run(
                command,  # Pass command as string instead of splitting
                shell=True,  # Add shell=True to preserve command structure
                capture_output=True,
                text=True,
            )
            
            # Get the output (stdout if available, stderr if stdout is empty)
            output = result.stdout if result.stdout else result.stderr
            
            # Check if command was successful (return code 0 means success)
            success = result.returncode == 0
            
            if success:
                return True, output
            else:
                return False, f"Command '{command}' failed with error:\n{output}"
                
        except Exception as e:
            return False, f"Error executing command '{command}': {str(e)}"

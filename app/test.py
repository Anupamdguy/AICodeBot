import os
import subprocess

# Get the current user's name
current_user = os.getlogin()

print(f"The script is being run by: {current_user}")

# Check group memberships (Windows)
try:
    result = subprocess.run(['whoami', '/groups'], capture_output=True, text=True, check=True)
    print("Group memberships and permissions:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Error checking group memberships:", e)
import os
import requests
from scientiflow_cli.cli.auth_utils import getAuthToken

def logout_user():
    app_base_url = "https://www.backend.scientiflow.com/api"
    logout_url = f"{app_base_url}/auth/logout"
    token = getAuthToken()
    if token:
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.post(logout_url, headers=headers)
        if response.status_code == 200:
            print("Logout successful!")
            token_file_path = os.path.expanduser("~/.scientiflow/token")
            key_file_path = os.path.expanduser("~/.scientiflow/key")
            os.remove(token_file_path)
            os.remove(key_file_path)
            print("Token and key files deleted.")
        else:
            print("Logout failed!")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
    else:
        print("Token file not found or decryption failed. Please login to continue.")
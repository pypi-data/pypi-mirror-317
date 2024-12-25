import requests
from scientiflow_cli.cli.auth_utils import getAuthToken

API_BASE = "https://www.backend.scientiflow.com/api"

def init_output():
    try:
        with open("output.txt", 'w') as f:
            f.write('')
    except:
        pass

def capture_output(text: str):
    try:
        with open("output.txt", 'a') as f:
            f.write(text+"\n")
        print(text+"\n")
    except:
        pass

def update_terminal_output(project_job_id: int):
    try:
        with open("output.txt", 'r') as f:
            terminal_output = f.read()
    except:
        pass
    headers = { "Authorization": f"Bearer {getAuthToken()}"}
    body = {"project_job_id": project_job_id, "terminal_output": terminal_output}
    res = requests.post(f"{API_BASE}/agent-application/update-terminal-output", headers=headers, data=body)
    print("[+] Terminal output updated successfully.")

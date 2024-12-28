import requests
from scientiflow_cli.cli.auth_utils import getAuthToken

API_BASE = "https://www.backend.scientiflow.com/api"

def update_job_status(project_job_id: int, status: str):
    headers = { "Authorization": f"Bearer {getAuthToken()}"}
    body = {"project_job_id": project_job_id, "status": status}
    res = requests.post(f"{API_BASE}/agent-application/update-project-job-status", headers=headers, data=body)
    print("[+] Project status updated successfully.")
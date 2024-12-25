import requests
import os
#from scientiflow_cli.cli.login import login_user, user_has_auth_token, get_auth_token

app_base_url = "https://www.backend.scientiflow.com/api"


def handle_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

def make_request(method, data, use, url=app_base_url):
    try:
        if method == 'GET':
            if use == "Check Jobs To Execute":
                response = requests.get(url+"/agent-application/check-jobs-to-execute")
            elif use == "Get Tar Gz File":
                response = requests.get(url+"/agent-application/get-tar-gz-file")
            elif use == "Get User Containers":
                response = requests.get(url+"/agent-application/get-user-containers")
        elif method == 'POST':
            if use == 'Login':
                response = requests.post(url+"/auth/login", json=data)
            elif use == 'Logout':
                response = requests.post(url+"/auth/logout", json=data)
            elif use == "update project job status":
                response = requests.post(url+"/agent-application/update-project-job-status", json=data)
            elif use == "update terminal output":
                response = requests.post(url+"/agent-application/update-terminal-output", json=data)
        return handle_response(response)
    except requests.RequestException as e:
        return "Unsupported HTTP method"

        

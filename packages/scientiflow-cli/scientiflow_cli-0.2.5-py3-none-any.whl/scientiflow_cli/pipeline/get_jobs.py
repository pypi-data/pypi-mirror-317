import requests
from pathlib import Path


API_BASE = "https://www.backend.scientiflow.com/api"


def get_jobs(auth_token: str) -> list[dict]:
    headers = { "Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{API_BASE}/agent-application/check-jobs-to-execute", headers=headers)
    
    if not response.status_code == 200:
        print("Error fetching jobs - Invalid response")
        return []
    
    try:
        jobs = response.json()
        # breakpoint()
        if len(jobs) == 0:
            print("No jobs to execute")
            return []
        else:
            print("\n{:<20} {:<20} {:<20}".format("Project Job ID", "Project Title", "Job Title"))
            print("===============      =============        =========")
            # for index, job in enumerate(response.json(), start=1):
            for job in response.json():
                project_job_id: int = job['project']['id']
                project_title: str = job['project']['project_title']
                job_title: str = job['project_job']['job_title']
                print("{:<20} {:<20} {:<20}".format(project_job_id, project_title, job_title))
            print("\n")
            return jobs

    except requests.exceptions.JSONDecodeError:
        print("Error fetching jobs - Invalid JSON")
        return []

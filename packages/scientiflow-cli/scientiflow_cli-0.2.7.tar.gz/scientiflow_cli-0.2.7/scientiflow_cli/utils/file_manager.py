import io
import os
import tarfile
import requests
from pathlib import Path


API_BASE = "https://www.backend.scientiflow.com/api"


def get_job_files(auth_token: str, job: dict) -> None:
    base_dir: str =  job['server']['base_directory']
    # project_id = job['project']['id']
    project_job_id = job['project_job']['id']
    project_name = job['project']['project_title']
    job_dir = job['project_job']['job_directory']

    # if os.getenv("SCFLOW_DEBUG", ""):
    #     project_id = 3

    headers = { "Authorization": f"Bearer {auth_token}"}
    params = { "project_job_id": project_job_id }

    print("[+] Fetching user files... ", end="")
    response = requests.get(f"{API_BASE}/agent-application/get-tar-gz-file", headers=headers, params=params)

    if response.status_code == 200:
        print("Done")
        project_dir_name = Path(base_dir) / project_name
        job_dir_name = project_dir_name / job_dir
        job_dir_name.mkdir(parents=True, exist_ok=True)

        print("[+] Extracting user files... ", end="")
        tar_data = io.BytesIO(response.content)

        with tarfile.open(fileobj=tar_data, mode="r:gz") as tar:
            # tar.extractall(path = project_dir_name)
            for member in tar.getmembers():
                file_path = project_dir_name / member.name
                if file_path.is_file() and file_path.exists():
                    file_path.unlink()

                tar.extract(member, path=job_dir_name)

        print("Done")
        print(f"[+] Files extracted to {project_dir_name}")
    
    elif response.status_code == 403:
        print("[X] User does not have any files")

    else:
        print("Error fetching user files")
        return
    


def create_job_dirs(job: dict) -> None:
    """
        Job should be a dict with all the fields.
        Import mock_job from mock.py to test these functions.
    """
    base_dir = Path(job['server']['base_directory'])
    project_dir = base_dir / job['project']['project_title']
    job_dir = project_dir / job['project_job']['job_directory']

    # Clear the job directory if it already exists, regardless of the new_job flag
    # if job['new_job']:
    # if job_dir.exists():
        # clear_directory(job_dir)

    job_dir.mkdir(parents=True, exist_ok=True)



def clear_directory(dir_root: Path):
    for root, dirs, files in dir_root.walk(top_down=False):
        for name in files:
            (root / name).unlink()
        for name in dirs:
            (root / name).rmdir()
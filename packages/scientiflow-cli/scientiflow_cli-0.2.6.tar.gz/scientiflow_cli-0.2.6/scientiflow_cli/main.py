import os
import argparse
from scientiflow_cli.cli.login import login_user#, user_has_auth_token, get_auth_token
from scientiflow_cli.cli.login import login_user
from scientiflow_cli.cli.logout import logout_user
from scientiflow_cli.pipeline.get_jobs import get_jobs
from scientiflow_cli.utils.file_manager import create_job_dirs, get_job_files
from scientiflow_cli.pipeline.container_manager import get_job_containers
from scientiflow_cli.utils.mock import mock_jobs
from scientiflow_cli.services.executor import execute_jobs, execute_jobs_sync, execute_job_id
from scientiflow_cli.cli.auth_utils import getAuthToken
from scientiflow_cli.utils.singularity import install_singularity_main as install_singularity


AUTH_TOKEN = os.getenv("AUTH_TOKEN", None)

def main():
    parser = argparse.ArgumentParser(description="Scientiflow Agent CLI")
    parser.formatter_class = lambda prog: argparse.HelpFormatter(prog, max_help_position=50)

    parser.add_argument('--login', action='store_true', help="Login using your scientiflow credentials")
    parser.add_argument('--logout', action='store_true', help="Logout from scientiflow")
    parser.add_argument('--list-jobs', action='store_true', help="Get jobs to execute")
    parser.add_argument('--execute-jobs', action='store_true', help="Fetch and execute pending jobs")
    parser.add_argument('--execute-jobs-sync', action='store_true', help="Fetch and execute pending jobs synchronously in order of their job id")
    parser.add_argument('--execute-job-by-id', type=int, dest='Job_ID', help="Fetch and execute job with a specific job id")
    parser.add_argument('--install-singularity', action='store_true', help="Install Singularity")
    args = parser.parse_args()


    try:
        # We're checking here that if command is either login or logout, then we don't need to check for auth token
        # since these two are the only two commands allowed to run without an auth token
        # if not args.login and not args.logout:
        #     print("Session not found. Please login to continue")
        #     return

        if args.login:
            login_user()
        
        elif args.logout:
            logout_user()

        elif args.list_jobs:
            get_jobs(auth_token = getAuthToken())

        elif args.execute_jobs:
            execute_jobs(auth_token=getAuthToken())
            
        elif args.execute_jobs_sync:
            execute_jobs_sync(auth_token=getAuthToken())

        elif args.Job_ID:
            execute_job_id(auth_token=getAuthToken(), job_id = args.Job_ID)

        elif args.install_singularity:
            install_singularity()

        else:
            print("No arguments specified. Use --help to see available options")
    
    except Exception as e:
        print("Error: ", e)
        return


if __name__ == "__main__":
    main()
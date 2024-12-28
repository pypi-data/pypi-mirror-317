import subprocess
import re
from typing import Dict, List, Any
from scientiflow_cli.services.status_updater import update_job_status
from scientiflow_cli.services.terminal_updater import init_output, capture_output, update_terminal_output

class PipelineExecutor:
    def __init__(self, base_dir: str, project_job_id: int, project_title: str, job_dir_name: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, str]], environment_variables: Dict[str, str]):
        self.base_dir = base_dir
        self.project_job_id = project_job_id
        self.project_title = project_title
        self.job_dir_name = job_dir_name
        self.nodes = nodes
        self.edges = edges
        self.environment_variables = environment_variables

        # Create a mapping of nodes
        self.nodes_map = {node['id']: node for node in nodes}

        # Create adjacency list based on edges
        self.adj_list = {node['id']: [] for node in nodes}
        for edge in edges:
            self.adj_list[edge['source']].append(edge['target'])

        # Find the root (the node with no incoming edges)
        all_nodes = set(self.nodes_map.keys())
        target_nodes = {edge['target'] for edge in edges}
        self.root_nodes = all_nodes - target_nodes

    def replace_variables(self, command: str) -> str:
        # Function to replace each match with the corresponding value from the dictionary
        def replacer(match):
            variable_name = match.group(1)  # Extract the variable name (without ${})
            return self.environment_variables.get(variable_name, f"${{{variable_name}}}")

        pattern = r'\$\{(\w+)\}'  # This regex pattern finds placeholders like ${<variable>}
        result = re.sub(pattern, replacer, command)
        return result

    def execute_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
            capture_output(result.stdout)
        except subprocess.CalledProcessError as e:
            capture_output(f"Error: {e.stderr} \nTerminating the program.")
            update_job_status(self.project_job_id, "failed")
            update_terminal_output(self.project_job_id)
            raise SystemExit("An error occurred and the program has been terminated.")
        return

    def dfs(self, node: str):
        current_node = self.nodes_map[node]
        
        if current_node['type'] == "splitterParent":
            collector = None
            for splitter_child in self.adj_list[node]:
                if self.nodes_map[splitter_child]['data']['active'] == True:
                    collector = self.dfs(splitter_child)
            else:
                if collector and self.adj_list[collector]:
                    return self.dfs(self.adj_list[collector][0])
                else:
                    return

        elif current_node['type'] == "splitter-child":
            if current_node['data']['active'] == True:
                if self.adj_list[node]:
                    return self.dfs(self.adj_list[node][0])
                else:
                    return

        elif current_node['type'] == "terminal":
            commands = current_node['data']['commands']
            isGPUEnabled = False
            try:
                isGPUEnabled = current_node['data']['gpuEnabled']
            except:
                isGPUEnabled = False
            for command in commands:
                cmd = self.replace_variables(command.get('command'))
                if cmd:
                    if isGPUEnabled:
                        self.execute_command(f"cd {self.base_dir}/{self.project_title}/{self.job_dir_name} && singularity exec --nv --nvccli {self.base_dir}/containers/{current_node['data']['software']}.sif {cmd}")
                    else:
                        self.execute_command(f"cd {self.base_dir}/{self.project_title}/{self.job_dir_name} && singularity exec {self.base_dir}/containers/{current_node['data']['software']}.sif {cmd}")
            if self.adj_list[node]:
                return self.dfs(self.adj_list[node][0])
            else:
                return

        elif current_node['type'] == "collector":
            if self.adj_list[node]:
                return node
            else:
                return

    def decode_and_execute_pipeline(self):
        update_job_status(self.project_job_id, "running")
        if self.root_nodes:
            # Start DFS from the first root node
            root_node = next(iter(self.root_nodes))
            self.dfs(root_node)
        update_job_status(self.project_job_id, "completed")

# External function to initiate the pipeline execution
def decode_and_execute_pipeline(base_dir: str, project_job_id: int, project_title: str, job_dir_name: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, str]], environment_variables: Dict[str, str]):
    executor = PipelineExecutor(base_dir, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables)
    init_output()
    executor.decode_and_execute_pipeline()
    update_terminal_output(project_job_id)
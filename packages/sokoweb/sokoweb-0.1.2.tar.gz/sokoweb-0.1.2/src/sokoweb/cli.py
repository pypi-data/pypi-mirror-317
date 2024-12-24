from dotenv import load_dotenv
import subprocess
import sys
import os

def main():
    load_dotenv()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
    
    subprocess.run([
        "docker",
        "compose",
        "-f",
        os.path.join(project_dir, "docker-compose.yml"),
        "up",
        "--build"
    ], check=True)
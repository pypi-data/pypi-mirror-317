from dotenv import load_dotenv
import subprocess
import sys
import os

def main():
    # Load environment variables from .env
    load_dotenv()

    # Run docker compose up --build
    # Docker Compose will automatically read .env unless overridden
    subprocess.run(["docker", "compose", "up", "--build"], check=True)
    
    # Note: Remove check=True to run in background
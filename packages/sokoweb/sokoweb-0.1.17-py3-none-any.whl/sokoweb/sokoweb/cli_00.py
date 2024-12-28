# File: cli.py
import os
import subprocess
import sys
import shutil
import tempfile
import re
from pathlib import Path
from importlib import resources  # Python 3.9+

def read_existing_env(env_path):
    existing_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    existing_vars[key.strip()] = value.strip()
    return existing_vars

def validate_port(port):
    try:
        port = int(port)
        return 1024 <= port <= 65535
    except ValueError:
        return False

def validate_hostname(hostname):
    if not hostname:
        return False
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}|[a-zA-Z0-9\.-]+$')
    return bool(ip_pattern.match(hostname))

def prompt_for_three_vars(existing_vars):
    """Prompt ONLY for NODE_PORT, NODE_TCP_PORT, ADVERTISE_IP.
    If user hits Enter, keep existing .env value or use defaults."""
    
    # 1) NODE_PORT
    default_node_port = existing_vars.get('NODE_PORT', '8000')
    while True:
        node_port = input(
            f"Enter NODE_PORT (press Enter for default {default_node_port}): "
        ).strip()
        if not node_port:
            node_port = default_node_port
        if validate_port(node_port):
            existing_vars["NODE_PORT"] = node_port
            break
        print("Invalid port! Must be between 1024 and 65535.")

    # 2) NODE_TCP_PORT
    default_tcp_port = existing_vars.get('NODE_TCP_PORT', '8500')
    while True:
        node_tcp_port = input(
            f"Enter NODE_TCP_PORT (press Enter for default {default_tcp_port}): "
        ).strip()
        if not node_tcp_port:
            node_tcp_port = default_tcp_port
        if validate_port(node_tcp_port):
            existing_vars["NODE_TCP_PORT"] = node_tcp_port
            break
        print("Invalid port! Must be between 1024 and 65535.")

    # 3) ADVERTISE_IP
    default_ip = existing_vars.get('ADVERTISE_IP', 'localhost')
    while True:
        advertise_ip = input(
            f"Enter ADVERTISE_IP (e.g., example.com) [default {default_ip}]: "
        ).strip()
        if not advertise_ip:
            advertise_ip = default_ip
        if validate_hostname(advertise_ip):
            existing_vars["ADVERTISE_IP"] = advertise_ip
            break
        print("Invalid hostname/IP! Please enter a valid hostname or IP address.")

def write_env(env_path, vars_dict):
    try:
        with open(env_path, 'w') as f:
            for k, v in vars_dict.items():
                f.write(f"{k}={v}\n")
    except Exception as e:
        print(f"Error writing .env: {e}")
        sys.exit(1)

def up():
    print("\nSetting up environment variables...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Copy Dockerfile + docker-compose.yml from inside the package
        docker_dir = resources.files("sokoweb.docker")
        shutil.copyfile(docker_dir / "Dockerfile", temp_path / "Dockerfile")
        shutil.copyfile(docker_dir / "docker-compose.yml", temp_path / "docker-compose.yml")

        # Now handle the .env. If user already has .env in their project,
        # you might want to let them specify the path. Or we can start empty.
        env_path = temp_path / ".env"

        # If you want to load an existing .env from the user's current directory,
        # you can copy that in if it exists:
        user_env = Path.cwd() / ".env"
        if user_env.exists():
            shutil.copyfile(user_env, env_path)

        existing_vars = read_existing_env(env_path)
        # Prompt ONLY for the 3 required variables (others remain from .env)
        prompt_for_three_vars(existing_vars)

        # Write them back
        write_env(env_path, existing_vars)

        print("\nUpdated environment variables (from .env in the temp directory):")
        for k, v in existing_vars.items():
            print(f"{k}={v}")

        # Start Docker
        print("\nStarting Docker containers...")
        try:
            process = subprocess.run(
                ["docker", "compose", "-f", "docker-compose.yml", "up", "--build"],
                check=True,
                cwd=str(temp_path)
            )
            if process.returncode == 0:
                print("Successfully started Docker containers.")
        except subprocess.CalledProcessError as e:
            print(f"Error starting Docker containers (exit code={e.returncode})")
            sys.exit(e.returncode)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            sys.exit(1)

def down():
    """Stop/remove containers. For simplicity, runs a global 'docker compose down -v'."""
    print("Stopping Docker containers and removing volumes...")
    try:
        subprocess.run(["docker", "compose", "down", "-v"], check=True)
        print("Successfully stopped and removed containers/volumes.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Docker containers (exit code={e.returncode})")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    up()
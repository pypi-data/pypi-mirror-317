import os
import subprocess
import sys
from pathlib import Path
import re
import tempfile
import shutil

# For Python 3.9+: from importlib import resources
# If needing backward compatibility, use importlib_resources from PyPI.
from importlib import resources

def validate_port(port):
    try:
        port = int(port)
        return 1024 <= port <= 65535
    except ValueError:
        return False

def validate_hostname(hostname):
    if not hostname:
        return False
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$|^[a-zA-Z0-9.\-]+$')
    return bool(ip_pattern.match(hostname))

def prompt_env_vars():
    """Prompt user for environment variables, returning a dict of them."""
    env_vars = {}

    # NODE_PORT
    while True:
        node_port = input("Enter NODE_PORT (press Enter for default 8000): ").strip()
        if not node_port:
            node_port = "8000"
        if validate_port(node_port):
            env_vars["NODE_PORT"] = node_port
            break
        print("Invalid port! Please enter a number between 1024 and 65535.")

    # NODE_TCP_PORT
    while True:
        node_tcp_port = input("Enter NODE_TCP_PORT (press Enter for default 8500): ").strip()
        if not node_tcp_port:
            node_tcp_port = "8500"
        if validate_port(node_tcp_port):
            env_vars["NODE_TCP_PORT"] = node_tcp_port
            break
        print("Invalid port! Please enter a number between 1024 and 65535.")

    # ADVERTISE_IP
    while True:
        advertise_ip = input("Enter ADVERTISE_IP (e.g., ec2.aws...com): ").strip()
        if not advertise_ip:
            # If user just hits Enter, default to "localhost"
            advertise_ip = "localhost"
        if validate_hostname(advertise_ip):
            env_vars["ADVERTISE_IP"] = advertise_ip
            break
        print("Invalid hostname/IP! Please enter a valid hostname or IP address.")

    return env_vars

def write_env_file(env_vars, env_path):
    """Write user-supplied env vars to .env file."""
    try:
        with open(env_path, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

        print("\nUpdated environment variables:")
        for key, value in env_vars.items():
            print(f"{key}={value}")
    except Exception as e:
        print(f"Error writing to .env file: {str(e)}")
        sys.exit(1)

def up():
    """Start the Docker containers using the Docker artifacts embedded in the package."""
    # 1) Prompt the user for environment variables
    print("\nSetting up environment variables...")
    env_vars = prompt_env_vars()

    # 2) Create a temporary directory to hold Dockerfile, docker-compose.yml, .env
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # 3) Extract embedded Docker files from the package
        # 'sokoweb.docker' is the subpackage/folder containing Dockerfile, docker-compose.yml
        docker_resources = resources.files("sokoweb.docker")

        # Copy Dockerfile
        dockerfile_src = docker_resources / "Dockerfile"
        dockerfile_dest = temp_path / "Dockerfile"
        shutil.copyfile(dockerfile_src, dockerfile_dest)

        # Copy docker-compose.yml
        compose_src = docker_resources / "docker-compose.yml"
        compose_dest = temp_path / "docker-compose.yml"
        shutil.copyfile(compose_src, compose_dest)

        # 4) Write .env
        env_file_path = temp_path / ".env"
        write_env_file(env_vars, env_file_path)

        print("\nStarting Docker containers...")
        # 5) Run docker compose from the temp_dir
        try:
            process = subprocess.run(
                ["docker", "compose", "-f", str(compose_dest), "up", "--build"],
                check=True,
                cwd=str(temp_path)  # build context = temp_path
            )
            if process.returncode == 0:
                print("Successfully started Docker containers")
        except subprocess.CalledProcessError as e:
            print(f"Error starting Docker containers (exit code {e.returncode})")
            sys.exit(e.returncode)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            sys.exit(1)

def down():
    """Stop and remove Docker containers, volumes—using the same approach or any approach you like."""
    # In a more advanced scenario, you'd track the ephemeral location or store the Docker data in a known place.
    # For simplicity, let's just do a global approach: "docker compose down -v" from ANY compose file named "docker-compose.yml" in current dir or so.
    # Or you can replicate the approach above with the embedded compose file, if you prefer.
    print("Stopping Docker containers and removing volumes...")
    try:
        subprocess.run(["docker", "compose", "down", "-v"], check=True)
        print("Successfully stopped and removed Docker containers and volumes")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Docker containers (exit code {e.returncode})")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    up()
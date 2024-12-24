from dotenv import load_dotenv
import subprocess
import os
from importlib.resources import files  # Python 3.9+

def main():
    # Load environment variables from packaged .env
    env_path = files("sokoweb").joinpath(".env")
    if env_path.is_file():
        load_dotenv(str(env_path))
    else:
        print("Warning: .env file not found in installed package; using environment defaults.")

    # Load docker-compose configuration
    compose_path = files("sokoweb").joinpath("docker-compose.yml")
    if not compose_path.is_file():
        print("Error: docker-compose.yml not found in installed package.")
        return

    # Execute docker compose with packaged configuration
    subprocess.run([
        "docker",
        "compose",
        "-f", str(compose_path),
        "up",
        "--build"
    ], check=True)
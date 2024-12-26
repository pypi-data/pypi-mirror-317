import os
import subprocess
import time
import platform
import shutil

def check_and_install_docker():
    try:
        # Check if Docker is installed
        subprocess.check_call(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Docker is installed.")
    except FileNotFoundError:
        # Docker is not installed
        print("Docker is not installed.")
        if platform.system() == "Linux":
            print("\nTo install Docker on Linux, run the following commands:")
            print("1. Download Docker installation script:")
            print("   curl -fsSL https://get.docker.com -o get-docker.sh")
            print("\n2. Run the script with sudo:")
            print("   sudo sh get-docker.sh\n")
        elif platform.system() == "Windows":
            print("\nTo install Docker on Windows, download Docker Desktop from:")
            print("https://www.docker.com/products/docker-desktop\n")
        exit(1)

def check_and_start_docker():
    try:
        # Check if Docker is running
        subprocess.check_call(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Docker engine is running.")
    except subprocess.CalledProcessError:
        # Docker is installed but not running
        if platform.system() == "Linux":
            print("\nDocker is installed but not running. Attempting to start Docker service...")
            try:
                subprocess.check_call(["sudo", "systemctl", "start", "docker"])
                print("Docker service started successfully.")
            except subprocess.CalledProcessError:
                print("Failed to start Docker. Please start the Docker service manually using:")
                print("sudo systemctl start docker\n")
                exit(1)
        elif platform.system() == "Windows":
            print("\nDocker Desktop is not running. Please start Docker Desktop manually.")
            print("Open Docker Desktop from the Start menu and ensure the engine is running.")
            exit(1)

def build_and_run_mysql_container():
    container_name = "my-persistent-mysql"
    image_name = "apsitv27-mysql"
    volume_name = "mysql_data"
    mysql_root_password = "1234"

    try:
        # Step 1: Check if the image exists
        try:
            existing_image = subprocess.check_output([
                "docker", "images", "-q", image_name
            ]).strip().decode()
        except subprocess.CalledProcessError:
            existing_image = None

        # Build the Docker image only if it doesn't exist
        if not existing_image:
            print("Building the Docker image (this may take a few seconds)...")
            subprocess.check_call(
                ["docker", "build", "-t", image_name, os.path.dirname(__file__)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            print("Docker image already exists. Skipping build.")

        # Step 2: Check if the container exists
        try:
            existing_container = subprocess.check_output([
                "docker", "ps", "-aq", "--filter", f"name={container_name}"
            ]).strip().decode()
        except subprocess.CalledProcessError:
            existing_container = None

        # Step 3: Stop and remove existing container (if needed)
        if existing_container:
            print(f"Stopping and removing existing container '{container_name}'...")
            subprocess.check_call(["docker", "rm", "-f", container_name])

        # Step 4: Run a new container interactively (attached mode)
        print(f"Running a new container '{container_name}' with persistent volume '{volume_name}'...")
        subprocess.check_call([
            "docker", "run", "-it", "--name", container_name, "-v",
            f"{volume_name}:/var/lib/mysql", "-e", f"MYSQL_ROOT_PASSWORD={mysql_root_password}", image_name
        ])

    except KeyboardInterrupt:
        # Gracefully handle CTRL+C
        print("\nProcess interrupted by the user. Exiting...")
        try:
            print(f"Stopping the container '{container_name}'...")
            subprocess.check_call(["docker", "rm", "-f", container_name])
            print(f"Container '{container_name}' stopped.")
        except subprocess.CalledProcessError:
            print(f"Error stopping the container '{container_name}'.")
        finally:
            exit(0)

if __name__ == "__main__":
    # Check if Docker is installed
    check_and_install_docker()

    # Ensure Docker is running
    check_and_start_docker()

    # Build and run MySQL container
    build_and_run_mysql_container()

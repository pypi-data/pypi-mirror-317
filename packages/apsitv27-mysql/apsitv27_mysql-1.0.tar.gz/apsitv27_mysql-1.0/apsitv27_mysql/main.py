import subprocess
import pkg_resources
import os
import time
import sys


def check_and_install_docker():
    try:
        # Check if Docker is installed by running 'docker --version'
        subprocess.check_call(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Docker is already installed.")
    except subprocess.CalledProcessError:
        print("Docker is not installed.")
        if sys.platform == "linux" or sys.platform == "linux2":
            print("Attempting to install Docker on Linux...")
            install_script_path = os.path.join(os.path.dirname(__file__), "install_docker.sh")
            if os.path.exists(install_script_path):
                subprocess.check_call(["bash", install_script_path])
            else:
                print("Error: install_docker.sh not found.")
        elif sys.platform == "win32":
            print("Docker is not installed.")
            print("Please install Docker Desktop for Windows from https://www.docker.com/products/docker-desktop")
        else:
            print("Docker installation is not supported on this platform automatically.")


def build_and_run_mysql_container():
    # Locate the Dockerfile and entrypoint.sh
    dockerfile_path = pkg_resources.resource_filename("apsitv27_mysql", "Dockerfile")
    entrypoint_path = pkg_resources.resource_filename("apsitv27_mysql", "entrypoint.sh")

    if not os.path.exists(dockerfile_path) or not os.path.exists(entrypoint_path):
        print("Dockerfile or entrypoint.sh not found in the installed package.")
        return

    # Use the directory containing the Dockerfile as the build context
    build_context = os.path.dirname(dockerfile_path)

    # Check if Docker is installed
    try:
        subprocess.check_call(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Docker is not installed or not running.")
        return

    # Build the Docker image
    print("Building the Docker image...")
    try:
        subprocess.check_call([
            "docker", "build", "-t", "apsitv27-mysql", build_context
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error while building Docker image: {e}")
        return

    # The name of the container
    container_name = "apsitv27-mysql-container"

    # Check if the container already exists
    try:
        existing_container = subprocess.check_output([
            "docker", "ps", "-aq", "-f", f"name={container_name}"
        ], stderr=subprocess.PIPE).strip().decode('utf-8')

        if existing_container:
            print(f"Container '{container_name}' exists. Restarting MySQL directly...")

            # Stop the container if it's running
            running_container = subprocess.check_output([
                "docker", "ps", "-q", "-f", f"name={container_name}"
            ], stderr=subprocess.PIPE).strip().decode('utf-8')
            if running_container:
                subprocess.check_call(["docker", "stop", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Restart the container
            subprocess.check_call([
                "docker", "start", container_name
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            raise subprocess.CalledProcessError(1, "No existing container.")
    except subprocess.CalledProcessError:
        print(f"No existing container found. Creating a new one...")
        subprocess.check_call([
            "docker", "run", "-d",
            "--name", container_name,
            "-v", "mysql_data:/var/lib/mysql",
            "apsitv27-mysql"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait until MySQL is ready
    print("Waiting for MySQL to start...")
    max_retries = 10
    for _ in range(max_retries):
        try:
            subprocess.check_call([
                "docker", "exec", container_name, "mysqladmin", "ping", "-h", "localhost"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("MySQL is ready.")
            break
        except subprocess.CalledProcessError:
            print("MySQL is not ready yet. Retrying...")
            time.sleep(2)
    else:
        print("MySQL did not start within the expected time. Exiting.")
        return

    # Execute MySQL directly in the container
    try:
        subprocess.check_call([
            "docker", "exec", "-it", container_name, "mysql"
        ])
    finally:
        # Stop the container after exiting MySQL
        print(f"Stopping the container '{container_name}'...")
        subprocess.check_call(["docker", "stop", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Your main logic, call check_and_install_docker() before anything else
if __name__ == "__main__":
    check_and_install_docker()

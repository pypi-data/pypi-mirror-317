import subprocess
import pkg_resources
import os
import time

def build_and_run_mysql_container():
    # Locate the Dockerfile
    dockerfile_path = pkg_resources.resource_filename("apsitv27_mysql", "dockerfile")
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
    subprocess.check_call([
        "docker", "build", "-t", "apsitv27-mysql", build_context
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # The name of the container
    container_name = "apsitv27-mysql-container"

    # Check if the container already exists
    try:
        existing_container = subprocess.check_output([
            "docker", "ps", "-aq", "-f", f"name={container_name}"
        ], stderr=subprocess.DEVNULL).strip().decode('utf-8')

        if existing_container:
            print(f"Container '{container_name}' exists. Restarting MySQL directly...")
            
            # Stop the container if it's running
            running_container = subprocess.check_output([
                "docker", "ps", "-q", "-f", f"name={container_name}"
            ], stderr=subprocess.DEVNULL).strip().decode('utf-8')
            if running_container:
                subprocess.check_call(["docker", "stop", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Restart the container
            subprocess.check_call([
                "docker", "start", container_name
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            raise subprocess.CalledProcessError(1, "No existing container.")
    except subprocess.CalledProcessError:
        print(f"No existing container found. Creating a new one...")
        subprocess.check_call([
            "docker", "run", "-d",
            "--name", container_name,
            "-v", "mysql_data:/var/lib/mysql",
            "apsitv27-mysql"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait until MySQL is ready
    print("Waiting for MySQL to start...")
    max_retries = 10
    for _ in range(max_retries):
        try:
            subprocess.check_call([
                "docker", "exec", container_name, "mysqladmin", "ping", "-h", "localhost"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        subprocess.check_call(["docker", "stop", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

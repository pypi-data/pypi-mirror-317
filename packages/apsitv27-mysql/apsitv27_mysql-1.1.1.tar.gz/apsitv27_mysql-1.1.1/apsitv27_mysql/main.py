import os
import subprocess
import time

def build_and_run_mysql_container():
    container_name = "my-persistent-mysql"
    image_name = "apsitv27-mysql"
    volume_name = "mysql_data"
    mysql_root_password = "1234"

    # Step 1: Check if the image exists
    try:
        existing_image = subprocess.check_output([
            "docker", "images", "-q", image_name
        ]).strip().decode()
    except subprocess.CalledProcessError:
        existing_image = None

    # Build the Docker image only if it doesn't exist
    if not existing_image:
        print("Building the Docker image...")
        subprocess.check_call([
            "docker", "build", "-t", image_name, os.path.dirname(__file__)
        ])
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
        container_status = subprocess.check_output([
            "docker", "inspect", "-f", "{{.State.Running}}", container_name
        ]).strip().decode()
        if container_status == "true":
            print(f"Container '{container_name}' is already running.")
        else:
            print(f"Restarting existing container '{container_name}'...")
            subprocess.check_call(["docker", "start", container_name])
    else:
        print(f"Running a new container '{container_name}' with persistent volume '{volume_name}'...")
        subprocess.check_call([
            "docker", "run", "-dit", "--name", container_name, "-v",
            f"{volume_name}:/var/lib/mysql", "-e", f"MYSQL_ROOT_PASSWORD={mysql_root_password}", image_name
        ])

    # Step 4: Wait for MySQL to be ready
    print("Waiting for MySQL to start...")
    for _ in range(10):  # Retry for ~20 seconds
        try:
            subprocess.check_call([
                "docker", "exec", container_name,
                "mysqladmin", "ping", "-uroot", f"-p{mysql_root_password}"
            ])
            print("MySQL is ready.")
            break
        except subprocess.CalledProcessError:
            print("MySQL is not ready yet. Retrying...")
            time.sleep(2)
    else:
        print("MySQL failed to start. Exiting.")
        raise Exception("MySQL did not start in time.")

    # Step 5: Enter MySQL shell
    try:
        print(f"Entering MySQL shell inside the container '{container_name}'...")
        subprocess.check_call([
            "docker", "exec", "-it", container_name, "mysql"
        ])
    except subprocess.CalledProcessError as e:
        print(f"Error executing MySQL: {e}.")
    finally:
        print(f"Leaving MySQL shell. The container '{container_name}' will remain running in the background.")

if __name__ == "__main__":
    build_and_run_mysql_container()

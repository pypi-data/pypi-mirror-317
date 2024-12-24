import subprocess

def build_and_run_mysql_container():
    # Check if Docker is installed
    try:
        subprocess.check_call(["docker", "--version"])
    except subprocess.CalledProcessError:
        print("Docker is not installed or not running.")
        return

    # Build the Docker image
    print("Building the Docker image...")
    subprocess.check_call([
        "docker", "build", "-t", "apsitv27-mysql", "."
    ])

    # Check if the container already exists
    print("Checking for an existing container...")
    container_name = "apsitv27-mysql-container"
    try:
        existing_container = subprocess.check_output([
            "docker", "ps", "-aq", "-f", f"name={container_name}"
        ]).strip().decode('utf-8')

        if existing_container:
            # Check if the container is running
            running_container = subprocess.check_output([
                "docker", "ps", "-q", "-f", f"name={container_name}"
            ]).strip().decode('utf-8')

            if running_container:
                print(f"Container '{container_name}' is already running.")
            else:
                print(f"Container '{container_name}' exists but is stopped. Restarting it...")
                subprocess.check_call(["docker", "start", container_name])
        else:
            raise subprocess.CalledProcessError(1, "No existing container.")
    except subprocess.CalledProcessError:
        print(f"No existing container found. Creating a new one...")
        subprocess.check_call([
            "docker", "run", "-it",
            "--name", container_name,
            "-v", "mysql_data:/var/lib/mysql",
            "apsitv27-mysql"
        ])

from setuptools import setup, find_packages

setup(
    name="apsitv27-mysql",
    version="1.1.1",
    packages=find_packages(),
    include_package_data=True,  # Include data files specified in MANIFEST.in
    entry_points={
        "console_scripts": [
            "apsitv27-mysql=apsitv27_mysql.main:build_and_run_mysql_container"
        ],
    },
    install_requires=[
        "docker",
        "setuptools>=65.0.0",
    ],
    # Add the Dockerfile and entrypoint.sh here
    package_data={
        "apsitv27_mysql": ["Dockerfile", "entrypoint.sh","install_docker.sh", "install_docker.bat"]
    },
)

#!/bin/bash

# Function to check if a port is available
function check_port() {
    local port=$1
    (echo >/dev/tcp/localhost/$port) &>/dev/null && return 1 || return 0
}

# Try to bind to the first available port from the list
for port in {3306..3312}; do
    if check_port $port; then
        echo "Port $port is available. Starting MySQL on this port."
        export MYSQL_PORT=$port
        break
    fi
done

# Ensure a port was found; exit if none are available
if [ -z "$MYSQL_PORT" ]; then
    echo "No available ports found in the range 3306-3312. Exiting."
    exit 1
fi

# Ensure the MySQL data directory exists
MYSQL_DATA_DIR="/var/lib/mysql"
if [ ! -d "$MYSQL_DATA_DIR/mysql" ]; then
    echo "Initializing MySQL data directory..."
    mysqld --initialize-insecure --user=mysql --datadir=$MYSQL_DATA_DIR
else
    echo "MySQL data directory already initialized."
fi

# Start MySQL on the available port
echo "Starting MySQL on port $MYSQL_PORT..."
mysqld --port=$MYSQL_PORT --user=mysql --datadir=$MYSQL_DATA_DIR --skip-networking=0 --bind-address=0.0.0.0 &

# Wait for MySQL to fully start
sleep 10

# Check if MySQL started successfully
if mysqladmin ping -uroot --password=$MYSQL_ROOT_PASSWORD > /dev/null 2>&1; then
    echo "MySQL started successfully on port $MYSQL_PORT."
else
    echo "MySQL failed to start. Exiting."
    exit 1
fi

# Keep the container running by running the MySQL process in the foreground
exec mysql

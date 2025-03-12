# Use a specific Python version as the base image
# Refer to the Python Docker image tag documentation for versions: https://hub.docker.com/_/python
ARG PYTHON_VERSION=3.11.8
FROM python:${PYTHON_VERSION} AS base

# Prevent Python from writing .pyc files and enable unbuffered output for logs
# This ensures that logs are immediately visible and no unnecessary bytecode is generated.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container to /app
WORKDIR /app

# Copy and run the script to install SQL Server drivers
# The script will be executed to ensure the necessary drivers are installed for database connection
COPY install_sql_driver.sh /app/install_sql_driver.sh
RUN chmod +x ./install_sql_driver.sh && ./install_sql_driver.sh

# Create a non-privileged user for running the application to follow best practices
# More info: https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the requirements.txt file into the container and install dependencies
# Using a separate layer for dependencies allows Docker to cache these layers, speeding up future builds
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-privileged user to run the app
USER appuser

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that the application listens on
# This makes it possible for the host machine to access the containerized app
EXPOSE 8000

# Start the application using Gunicorn to serve the Django app
# Gunicorn will bind to all available IP addresses on port 8000
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--chdir", "project"]

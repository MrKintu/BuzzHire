# syntax=docker/dockerfile:1

# Use the official Python image as the base image
ARG PYTHON_VERSION=3.11.6
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install --fix-missing -y \
       gcc python3-dev python3-pip \
       libpq-dev binutils libproj-dev \
       gdal-bin build-essential libssl-dev \
       libffi-dev vim nginx sudo \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user that the app will run under.
# Ensure that the UID and GID are unique and not already in use.
ARG UID=10001
RUN useradd -r -u $UID -g 0 app_user

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate  \
    && pip install --upgrade pip  \
    && pip install -r requirements.txt"

# Copy the source code into the container.
COPY . .

# Create directories for logs and media files
RUN mkdir -p /app/media/jobs \
    && mkdir -p /app/media/personalities \
    && mkdir -p /app/media/resumes \
    && mkdir -p /app/logs

# Create log files
RUN touch logs/critical.log logs/debug.log logs/error.log logs/info.log logs/warning.log

# Change ownership of the app directory to a non-root user
RUN chown -R app_user:root /app
RUN usermod -aG sudo app_user

# Switch to the new user
USER app_user

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
SHELL ["/bin/bash", "-c"]
CMD source venv/bin/activate && venv/bin/gunicorn BuzzHire.wsgi --bind=0.0.0.0:8000

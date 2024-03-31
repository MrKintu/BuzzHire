# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.11.6
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Nano
RUN apt update
RUN apt -y upgrade
RUN apt install -y python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv virtualenvwrapper
RUN echo "export VIRTUALENVWRAPPER_PYTHON=/app/usr/bin/python3" >> ~/.bashrc
RUN echo "export WORKON_HOME=~/Env" >> ~/.bashrc
RUN "source /app/usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
RUN source ~/.bashrc

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create Virtual Environment
RUN mkvirtualenv venv

# Install Requirements
RUN python -m pip install -r requirements.txt

# Create the logs directory and log files
RUN mkdir -p /app/logs
RUN touch /app/logs/critical.log
RUN touch /app/logs/debug.log
RUN touch /app/logs/error.log
RUN touch /app/logs/info.log
RUN touch /app/logs/warning.log

RUN decativate
# Virtual environment ends

# Configure uWSGI
#RUN apt-get install python3-dev
#RUN mkdir -p /app/uwsgi

# Give appuser permission execute in directory
RUN chown -R appuser:appuser /app

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD uwsgi --http :8000 --home /app/venv --chdir /app -w BuzzHire.wsgi

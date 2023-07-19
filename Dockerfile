# While optional this tells the Docker builder of the version
# syntax=docker/dockerfile:1

# Base image for Python applications
# This image is particularly for a web server using uvicorn
FROM python:3.11-slim-bullseye

# Expose ports which is proxied via traefik
EXPOSE 80

# Update the based image to latest versions of packages
# python 3.10 seems to want python3-tk installed
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends gcc python3-dev build-essential libpq-dev python3-tk postgresql-client vim\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the files in the src directory which is the app package
# and the dependency matrix dedescribed by pyproject.toml
WORKDIR /opt
COPY ./src/. .

# Ask poetry to install all packages including the app
# not in virtual machine as we are in a container
# In prodduction add --no-dev to poetry installation
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# The app package will be located in /opt/appname so run
# uvicorn at this level so it sees the package
ENTRYPOINT ["uvicorn", "lab_mock:app", "--host=0.0.0.0", "--port=80", "--reload"]

# There can only be one CMD argument
CMD []

# Labels are used to identify the image
LABEL org.opencontainers.image.source="https://github.com/anomaly/lab-python-mock-server"
LABEL org.opencontainers.image.description="A Python web server using Flask"
LABEL org.opencontainers.image.licenses="Apache-2.0"
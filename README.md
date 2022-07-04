# Lab - Mock Python server
![Docker Pulls](https://img.shields.io/docker/pulls/anomalyhq/lab-python-mock-server)

Anomaly uses Python for all of their server side requirements. This lab providers a containerized version of the Python server that mocks the presence of a server and simply outputs a static page with a list of key value pairs that it obtains from the container's environment.

The purpose of this application is to test the fact that the container has access to the secrets passed into it via the Kubernetes secrets mechanism. This application serves as the test Python server for Anomaly's [Terraform lab for Linode](https://github.com/anomaly/lab-tf-linode).

> This application should never be used in production.

## Configuring the environment variables

The application serves a single `root` entry point and can be configured in `src/lab_mock/__init__.py` which has a Python dictionary that resembles

```python
_ENV_LIST = [
    {
        "name": "PostgreSQL",
        "description": "Postgres database credentials",
        "vars": [
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_HOST",
            "POSTGRES_PORT",
            "POSTGRES_DB",
        ]
    },
]
```

Each object of the array is contains:
- `name`: The name of the environment variable group
- `description`: A description of the environment variable group
- `vars`: An array of environment variable names that are part of the group

The entry point will fetch the value of each environment variable and output it as a key value pair, outputting `None` if a value is not found.

> Please ensure this list is kept in sync with the Terraform lab, unless of course you are using it for other purposes.

## Architecture

The application is built using the [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework and uses Jinja2 for templating.

It uses `asgiref` to create an `ASGI` wrapper for the Flask application.

## Resources

- [Deploying FastAPI apps with HTTPS powered by Traefik](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/) by Sebastián Ramírez
- [How to Inspect a Docker Image’s Content Without Starting a Container](https://www.howtogeek.com/devops/how-to-inspect-a-docker-images-content-without-starting-a-container/) by James Walker
- [Poetry sub packages](https://github.com/python-poetry/poetry/issues/2270), an open issue to support sub packages in Poetry, which will be handy in splitting up our code base further.
- [Using find namespaces or find namespace package](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#using-find-namespace-or-find-namespace-packages)

## License
Contents of this repository are licensed under the Apache 2.0 license.

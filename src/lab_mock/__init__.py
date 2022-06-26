"""Mock Python Server.

This is a minimal Python web application that uses Flask to 
render a template that displays a nominated server of environment
variables.

The purpose of this mock application is to validate that a desired
Docker/Kubernetes environment is running as desired by Anomaly labs.

Refer to https://github.com/anomaly/lab-tf-linode for more information.

A production grade Python application is documented at 
https://github.com/anomaly/lab-python-server

"""
__name__ = "lab_mock"

import os
from asgiref.wsgi import WsgiToAsgi

from flask import Flask
from jinja2 import Environment, PackageLoader, select_autoescape

wsgi_app = Flask(__name__)

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
    {
        "name": "Redis",
        "description": "Redis database credentials",
        "vars": [
            "REDIS_HOST",
            "REDIS_PORT",
        ]
    },
    {
        "name": "App",
        "description": "Application credentials",
        "vars": [
            "CSRF_SECRET"
        ]
    }
]

@wsgi_app.route('/')
def lab_mock():
    """
    The only endpoint made available by this application to 
    use a Jinaj2 template to render a list of environment variables.
    """
    jinja2_env = Environment(
        loader=PackageLoader(package_name="lab_mock"),
        autoescape=select_autoescape()
    )

    # Process each environment variable in the list
    # fetch the value from the environment and pass it
    # onto the template to render

    _TEMPLATE_VARS = []
    for env in _ENV_LIST:
        _TEMPLATE_VARS.append({
            "name": env["name"],
            "description": env["description"],
            "vars": [
                {
                    "name": var,
                    # If the environment var has the value
                    # use that or use None
                    "value": os.environ.get(var, None)
                } for var in env["vars"]
            ]
        })

    template = jinja2_env.get_template('index.jinja2')
    return template.render(ENVIRONMENT=_TEMPLATE_VARS)




# WSGI to ASGI middleware
# https://flask.palletsprojects.com/en/2.1.x/deploying/asgi/
app = WsgiToAsgi(wsgi_app)
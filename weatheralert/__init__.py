import os

from flask import Flask


def create_app(test_config=None):
    # creates the flask instance and configures the app
    app = Flask("weatheralert", instance_relative_config=True)
    # setting default configuration
    app.config.from_mapping(
        # to be made more secure doing deployment
        SECRET_KEY="dev",
        # location and name for the database
        DATABASE=os.path.join(app.instance_path, "weatheralert.sqlite"),
    )

    if test_config is None:
        # load our custom config file if it exists, store SECRET_KEY here
        app.config.from_pyfile("config.py", silent=True)

    else:
        # load test_config otherwise
        app.config.from_mapping(test_config)

    # ensures the existence of the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import weatheralert

    app.register_blueprint(weatheralert.bp)

    return app

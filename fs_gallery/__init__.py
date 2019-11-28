# Imports
import os

from flask import Flask
from fs_gallery.router import router


def create_app():
    # Application Factory.
    app = Flask(__name__, instance_relative_config=True)

    # Ensure the instance directory exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Load configuration, or create config file if not found.
    try:
        app.config.from_pyfile("config.py")
    except FileNotFoundError:
        app.config.from_mapping(
            SECRET_KEY='moranagwaycornadamangiebtlentrapcuria'
        )
        conffile = open(os.path.join(app.instance_path, 'config.py'), "w")
        conffile.write("SECRET_KEY = 'moranagwaycornadamangiebtlentrapcuria'\n")
        conffile.close()
        print("Using default config. Edit config.py before deployment.")
        pass

    # Initialize routes.
    router(app)

    # Return the created app.
    return app

# Imports
import os

from flask import Flask


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
        conffile = open(os.path.join(app.instance_path, 'config.py'), "w")
        conffile.write(
            '''
            """
            File containing configuration values for flask application fsGallery.
            """
            # Import os and define the basedir variable as the root directory of the flaskGallery app
            import os
            basedir = os.path.abspath(os.path.dirname(__file__))

            SECRET_KEY = 'moranagwaycornadamangiebtlentrapcuria'
            BASE_DIRECTORY = basedir
            UPLOAD_FOLDER = os.path.join(basedir, 'picuploads')
            DATABASE = os.path.join(basedir, 'flaskapp.sqlite')

            '''
        )
        conffile.close()
        app.config.from_pyfile("config.py")
        print("Using default config. Edit config.py before deployment.")
        pass

    try:
        os.makedirs(app.config["UPLOAD_FOLDER"])
    except OSError:
        pass

    # Seondary Imports
    from fs_gallery import database
    from fs_gallery.router import router
    # Initialize routes.
    router(app)

    # Initialize database.
    database.initapp(app)

    # Return the created app.
    return app

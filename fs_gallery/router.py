import os

# Import flask methods and decorators for route definition and resolution
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import send_from_directory
from flask import flash
from flask import g


# Routing functions.
def router(app):
    """
    Routing functions.

    Parameters
    ----------
    app : flask application
        App to define routes for.
    """

    # Index route.
    @app.route('/')
    @app.route('/index')
    def index():
        """
        Index Router Function.

        Returns
        -------
        str
            HTML content to be displayed.
        """
        return render_template('index.html', title='Home')

    # Login route.
    @app.route('/login', method=['GET'])
    def login():
        """
        Login Router Function

        Returns
        -------
        str
            HTML content to be displayed.
        """

        if g.user is not None:
            flash('You are already logged in!')
            return redirect(url_for('index'))
        else:
            return render_template('login.html', title='Log In')
    return

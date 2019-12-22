# Import flask methods and decorators for route definition and resolution
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import send_from_directory
from flask import flash
from flask import g

from . import database

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
        folders = [
            {
                'filename': 'image_01.jpg',
                'title': 'Plexiglass'
            },

            {
                'filename': 'image_06.jpg',
                'title': 'Watercolor'
            },

            {
                'filename': 'image_02.jpg',
                'title': 'Acrylic'
            },

            {
                'filename': 'image_03.jpg',
                'title': 'Sculpture'
            },

            {
                'filename': 'image_04.jpg',
                'title': 'Collage'
            },

            {
                'filename': 'image_05.jpg',
                'title': 'Gifting'
            }
        ]
        announcements = [
            {
                'filename': 'image_07.jpg',
                'title': 'Gallery Postarino',
                'body': 'Here is a description for ya.Here is a description for ya.Here is a description for ya.Here is a description for ya.Here is a description for ya.Here is a description for ya.Here is a description for ya.Here is a description for ya.Here is a description for ya.Here is a description for ya.Here is a description for ya.',
                'timestamp': '12/17/2019'
            },
            {
                'filename': 'image_06.jpg',
                'title': 'Gallery Postarino',
                'body': 'Here is a description for ya.',
                'timestamp': '12/17/2019'
            },
            {
                'filename': 'image_05.jpg',
                'title': 'Gallery Postarino',
                'body': 'Here is a description for ya.',
                'timestamp': '12/17/2019'
            },
            {
                'filename': 'image_04.jpg',
                'title': 'Gallery Postarino',
                'body': 'Here is a description for ya.',
                'timestamp': '12/17/2019'
            },
            {
                'filename': 'image_03.jpg',
                'title': 'Gallery Postarino',
                'body': 'Here is a description for ya.',
                'timestamp': '12/17/2019'
            },
            {
                'filename': 'image_02.jpg',
                'title': 'Gallery Postarino',
                'body': 'Here is a description for ya.',
                'timestamp': '12/17/2019'
            }
        ]

        return render_template('index.html', title='Home', folders=folders, announcements=announcements)

    # About route.
    @app.route('/about')
    def about():
        """
        About Router Function.

        Returns
        -------
        str
            HTML content to be displayed.
        """
        return render_template('about.html', title='About')

    # Login route.
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        Login Router Function

        Returns
        -------
        str
            HTML content to be displayed.
        """

        if 'user' not in g:
            g.user = None

        if g.user is not None:
            flash('You are already logged in!')
            return redirect(url_for('index'))
        return render_template('login.html', title='Log In')

    # Upload Getter
    @app.route('/uploads/<image>')
    def uploaded_file(image):
        """Upload Fetcher - returns a requested file from the uploads folder.

        Args:
            filename (str): Filename associated with the desired file.

        Returns:
            file: File requested from the uploads folder.
        """
        return send_from_directory(app.config['UPLOAD_FOLDER'], image)

    # Portfolio Getter
    @app.route('/portfolio/<tag>')
    def portfolio(tag):
        # insert statement:  db.execute('INSERT INTO posts (title, postdesc, imgfile, forsale, size, tags) VALUES ("The Title", "Here\'s a description, yaaaah yeet!","image_01.jpg", "True", "4 x 18 in.", "watercolor, gifting")')
        gallery = database.getdb().execute('SELECT * FROM posts;').fetchall()
        return render_template("gallery.html", title="Gallery", gallery=gallery)
    return

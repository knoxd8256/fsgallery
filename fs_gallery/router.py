# Import flask methods and decorators for route definition and resolution
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import send_from_directory
from flask import session
from PIL import Image
from PIL import ImageOps
import random
import string
import os
from . import database


# Routing functions.
def router(app):
    """
    Routing functions.

    Parameters
    ----------
    app : flask application
        App to define routes for.

    Returns
    -------
    routes :
        A set of routes for use within the Flask framework.
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
                'filename': 'img/plexiglass.jpg',
                'title': 'Plexiglass'
            },

            {
                'filename': 'img/watercolor.jpg',
                'title': 'Watercolor'
            },

            {
                'filename': 'img/acrylic.jpg',
                'title': 'Acrylic'
            },

            {
                'filename': 'img/sculpture.jpg',
                'title': 'Sculpture'
            },

            {
                'filename': 'img/collage.jpg',
                'title': 'Collage'
            },

            {
                'filename': 'img/gifting.jpg',
                'title': 'Gifting'
            }
        ]
        announcements = database.getdb().execute("SELECT * FROM announcements").fetchall()
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
        Login Router Function.

        Returns
        -------
        str
            HTML content to be displayed.
        """
        if request.method == 'POST':
            db = database.getdb()
            user = db.execute("SELECT * FROM flaskuser WHERE username=?", (request.form['username'],)).fetchone()
            if request.form["password"] == user["pword"]:
                session.clear()
                session["user_id"] = 'admin'
                return redirect(url_for('index'))
        return render_template('login.html', title='Log In')

    # Logout route
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        """
        Logout Router Function.

        Returns
        -------
        str
            HTML content to be displayed.
        """
        session.clear()
        return redirect(url_for('index'))

    # Upload Getter
    @app.route('/uploads/<image>')
    def uploaded_file(image):
        """
        Upload Fetcher - returns a requested file from the uploads folder.

        Params
        ----
            image (str): Filename associated with the desired file.

        Returns
        -------
            file: File requested from the uploads folder.
        """
        return send_from_directory(app.config['UPLOAD_FOLDER'], image)

    # Portfolio Getter
    @app.route('/portfolio/<tag>')
    def portfolio(tag):
        # insert statement:  db.execute('INSERT INTO posts (title, postdesc, imgfile, forsale, size, tags) VALUES ("The Title", "Here\'s a description, yaaaah yeet!","image_01.jpg", "True", "4 x 18 in.", "watercolor, gifting")')
        gallery = database.getdb().execute('SELECT * FROM posts WHERE tags LIKE("%{}%");'.format(tag)).fetchall()
        return render_template("gallery.html", title="Gallery", gallery=gallery)

    # Admin Panel
    @app.route('/adminpanel')
    def adpanel():
        """
        Router Function for the Administrator Panel

        Returns
        -------
        str
            HTML content to display.
        """
        if 'user_id' not in session or session['user_id'] != 'admin':
            return redirect(url_for('login'))
        return render_template('adminpanel.html')

    # Announcement Adder
    @app.route('/addann', methods=['GET', 'POST'])
    def addannouncement():
        if 'user_id' not in session or session['user_id'] != 'admin':
            return redirect(url_for('index'))
        if request.method == 'POST':
            db = database.getdb()
            extension = '.' + request.files["imgfile"].filename.split('.')[-1]
            post = dict(request.form)
            imgname = ''.join(random.choice(string.ascii_letters) for x in range(12))
            post['imgname'] = imgname + extension
            db.execute("INSERT INTO announcements (title, body, imgfile, stamp) VALUES (?, ?, ?, datetime('now'))", (post['title'], post['body'], post['imgname']))
            db.commit()
            path = os.path.join(app.config['UPLOAD_FOLDER'], post["imgname"])
            request.files['imgfile'].save(path)
            return redirect(url_for('index'))
        return render_template('addann.html')

    # Post Adder
    @app.route('/addpost', methods=['GET', 'POST'])
    def addpost():
        if 'user_id' not in session or session['user_id'] != 'admin':
            return redirect(url_for('index'))
        if request.method == 'POST':
            image = request.files['imgfile']
            tags = ','.join(request.form.getlist('tags'))
            realform = dict(request.form)
            realform['tags'] = tags
            realform['imgfile'] = image.filename
            db = database.getdb()
            extension = '.' + realform['imgfile'].split('.')[-1]
            imgname = ''.join(random.choice(string.ascii_letters) for x in range(12))
            realform['imgname'] = imgname + extension
            db.execute("INSERT INTO posts (title, postdesc, imgfile, forsale, size, tags) VALUES (?, ?, ?, ?, ?, ?)", (realform['title'], realform['postdesc'], realform['imgname'], realform['forsale'], realform['size'], realform['tags']))
            db.commit()
            path = os.path.join(app.config['UPLOAD_FOLDER'], realform["imgname"])
            image.save(path)
            with Image.open(path) as reimage:
                transposed = ImageOps.exif_transpose(reimage)
                transposed.save(path)
            return redirect(url_for('index'))
        return render_template('addpost.html', title='Add Post')

    # Post Remover Panel
    @app.route('/postdel')
    def postdel():
        if 'user_id' not in session or session['user_id'] != 'admin':
            return redirect(url_for('index'))
        gallery = database.getdb().execute("SELECT * FROM posts").fetchall()
        return render_template('postdel.html', title='Remove A Post', gallery=gallery)

    # Post Removal Route
    @app.route('/rempost/<id>')
    def rempost(id):
        if 'user_id' not in session or session['user_id'] != 'admin':
            return redirect(url_for('index'))
        db = database.getdb()
        post = db.execute('SELECT * FROM posts WHERE id=?', (id)).fetchone()
        path = os.path.join(app.config['UPLOAD_FOLDER'], post['imgfile'])
        os.remove(path)
        db.execute('DELETE FROM posts WHERE id=?', (id))
        db.commit()
        return redirect(url_for('postdel'))

    # Announcement Removal Panel
    @app.route('/anndel')
    def anndel():
        if 'user_id' not in session or session['user_id'] != 'admin':
            return redirect(url_for('index'))
        announcements = database.getdb().execute("SELECT * FROM announcements").fetchall()
        return render_template('anndel.html', title='Remove An Announcement', announcements=announcements)

    # Post Removal Route
    @app.route('/remann/<id>')
    def remann(id):
        if 'user_id' not in session or session['user_id'] != 'admin':
            return redirect(url_for('index'))
        db = database.getdb()
        db.execute('DELETE FROM announcements WHERE id=?', (id))
        db.commit()
        return redirect(url_for('anndel'))

    return

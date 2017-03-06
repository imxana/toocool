# 'microblog' is an example, change the model for your own.

from flask import g
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def register(app):

    db = SQLAlchemy(app)

    # flask command

    @app.cli.command('initdb')
    def initdb_command():
        """Initializes the database."""

        # Database initialization here
        db.create_all()
        print('Initialized the database.')



    @app.cli.command('testdb')
    def datatest_command():
        """Insert some data for testing."""
        admin = User('admin', 'admin@example.com', '123')
        guest = User('guest', 'guest@example.com', '456')
        db.session.add(admin)
        db.session.add(guest)
        py = Category('Python')
        p = Post('Hello Python!', 'Python is pretty cool', py)
        db.session.add(py)
        db.session.add(p)
        db.session.commit()
        print('OK')





    # Models defined here

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        password = db.Column(db.String(20))
        email = db.Column(db.String(120), unique=True)

        def __init__(self, username, email, psw):
            self.username = username
            self.email = email
            self.password = psw

        def __repr__(self):
            return '<User %r>' % self.username


    class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80))
        body = db.Column(db.Text)
        pub_date = db.Column(db.DateTime)

        category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
        category = db.relationship('Category',
                backref=db.backref('posts', lazy='dynamic'))

        def __init__(self, title, body, category, pub_date=None):
            self.title = title
            self.body = body
            if pub_date is None:
                pub_date = datetime.utcnow()
            self.pub_date = pub_date
            self.category = category

        def __repr__(self):
            return '<Post %r>' % self.title


    class Category(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return '<Category %r>' % self.name




    # Flask-admin initialization here

    admin = Admin(app, name='Admin', template_mode='bootstrap3')

    class GlobalView(ModelView):
        can_create = False
        can_edit = True
        can_delete = True
        can_view_details = True

    class UserView(GlobalView):
        # can_delete = False  # disable model deletion
        pass


    class PostView(GlobalView):
        page_size = 50  # the number of entries to display on the list view

    admin.add_view(UserView(User, db.session))
    admin.add_view(PostView(Post, db.session))
    admin.add_view(GlobalView(Category, db.session))






    # Request Lifecycle
    
    @app.before_request
    def before_request():
        g.db = db
        g.User = User
        g.Post = Post
        g.Category = Category

    # @app.teardown_request
    # def teardown_request():
        # db = getattr(g, 'db', None)
        # if db is not None:
            # db.close()
            # db = None
        # getattr(g,'User',None)=None
        # getattr(g,'Post',None)=None



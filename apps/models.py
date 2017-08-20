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
        # py = Category('Python')
        # p = Post('Hello Python!', 'Python is pretty cool', py)
        # db.session.add(py)
        # db.session.add(p)
        db.session.commit()
        print('OK')




    # Models defined here

    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        password = db.Column(db.String(80))
        email = db.Column(db.String(120), unique=True)

        create_time = db.Column(db.DateTime)
        del_status = db.Column(db.Boolean, default=False)

        def __init__(self, username, email, psw):
            self.username = username
            self.email = email
            self.password = psw

        def __repr__(self):
            return '<User %r>' % self.username

        # def get_items(self):
        #     return self.items.all()


    class FollowUser(db.Model):
        __tablename__ = 'follow_user'
        id = db.Column(db.Integer, primary_key=True)

        from_user_id = db.Column(db.Integer)#,  db.ForeignKey('user.id'))
        to_user_id = db.Column(db.Integer)#,  db.ForeignKey('user.id'))

        del_status = db.Column(db.Boolean, default=False)

        @property
        def from_user(self):
            return g.User.query.filter_by(del_status=False, id=self.from_user_id).first()

        @property
        def to_user(self):
            return g.User.query.filter_by(del_status=False, id=self.to_user_id).first()

        def __init__(self, to_user_id, from_user_id):
            self.from_user_id = from_user_id
            self.to_user_id = to_user_id


    class Item(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        url = db.Column(db.String(200))
        param = db.Column(db.String(2000), nullable=True) # including picture type

        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        user = db.relationship('User',
                backref=db.backref('items', lazy='dynamic'))

        create_time = db.Column(db.DateTime)
        del_status = db.Column(db.Boolean, default=False)

        def __init__(self, name, url, user_id=None, param=None):
            self.name = name
            self.url = url
            self.create_time = datetime.utcnow()
            if user_id:
                self.user_id = user_id
            if param:
                self.param = param

    # class Post(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     title = db.Column(db.String(80))
    #     body = db.Column(db.Text)
    #     pub_date = db.Column(db.DateTime)
    #
    #     category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #     category = db.relationship('Category',
    #             backref=db.backref('posts', lazy='dynamic'))
    #
    #     def __init__(self, title, body, category, pub_date=None):
    #         self.title = title
    #         self.body = body
    #         if pub_date is None:
    #             pub_date = datetime.utcnow()
    #         self.pub_date = pub_date
    #         self.category = category
    #
    #     def __repr__(self):
    #         return '<Post %r>' % self.title
    #
    #
    # class Category(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     name = db.Column(db.String(50))
    #
    #     def __init__(self, name):
    #         self.name = name
    #
    #     def __repr__(self):
    #         return '<Category %r>' % self.name
    #
    #
    #
    #
    #
    # # the docs descript
    #
    # class PictureList(db.Model):
    #     """docstring for PictureList."""
    #     pictureId = db.Column(db.Integer, primary_key=True)
    #     pictureUrl = db.Column(db.String(300))
    #     filterValue = db.Column(db.String(1000))
    #     posterValue = db.Column(db.String(1000))
    #     styleId = db.Column(db.Integer)
    #     createTime = db.Column(db.DateTime)
    #
    #     def __init__(self, pu, fv, pv, si, ct=None):
    #         super(PictureList, self).__init__()
    #         # self.arg = arg
    #         self.pictureUrl = pu
    #         self.filterValue = fv
    #         self.posterValue = pv
    #         self.styleId = si
    #         if ct is None:
    #             ct = datetime.utcnow()
    #         self.createTime = ct
    #
    # class StyleList(db.Model):
    #     """docstring for StyleList."""
    #     styleId = db.Column(db.Integer, primary_key=True)
    #     styleName = db.Column(db.String(50))
    #     styleImgUrl = db.Column(db.String(300))
    #     originImgUrl = db.Column(db.String(300))
    #     resultImgUrl = db.Column(db.String(300))
    #     isSystemDefault = db.Column(db.Boolean)
    #     createTime = db.Column(db.DateTime)
    #
    #     def __init__(self, sn, siu, oiu, riu, isd=False, ct=None):
    #         super(StyleList, self).__init__()
    #         self.styleName = sn
    #         self.styleImgUrl = siu
    #         self.originImgUrl = oiu
    #         self.resultImgUrl = riu
    #         self.isSystemDefault = isd
    #         if ct is None:
    #             ct = datetime.utcnow()
    #         self.createTime = ct
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
    admin.add_view(GlobalView(FollowUser, db.session))

    admin.add_view(GlobalView(Item, db.session))
    # admin.add_view(PostView(Post, db.session))
    # admin.add_view(GlobalView(Category, db.session))





    # Request Lifecycle

    @app.before_request
    def before_request():
        g.db = db
        g.User = User
        # g.Post = Post
        # g.Category = Category
        g.Item = Item
        g.FollowUser = FollowUser

    # @app.teardown_request
    # def teardown_request(exception=None):
    #     arr = ['db', 'User', 'Item']#['db', 'User', 'Post', 'Category', 'Item']
    #     for name in arr:
    #         delattr(g, name)

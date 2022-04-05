from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    @property
    def fullname(self):
        """Returns full name of user"""
        return f'{self.first_name} {self.last_name}'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String,
        nullable=False
    )
    last_name = db.Column(
        db.String,
        nullable=False
    )
    img_url = db.Column(
        db.String,
    )

    posts = db.relationship('Post', cascade='all, delete', backref='users')

class Post(db.Model):
    __tablename__ = 'posts'

    @property
    def date(self):
        """create nicer date format"""
        dt = self.created_at
        date = dt.strftime("%A, %d. %B %Y %I:%M%p")
        return date

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String,
        nullable=False
    )

    content = db.Column(
        db.String
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        # server_default = func.now()
        default = datetime.datetime.now
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    categories = db.relationship('PostTag', cascade='all, delete', backref='post')

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,  
    )

    name = db.Column(
        db.String,
        nullable=False
    )

    categories = db.relationship('Post', secondary='posts_tags', backref='tag')

class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True
    )

  
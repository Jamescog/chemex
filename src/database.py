from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Users(db.Model):
    """
        model class for user table
        Attributes:
            id(Integer) - primary key for the table
            firstName - first name of the user
            lastName - last name of the user
            username - username of the user
            email - email of the user
            password for the user
            role - the role for ther user.
            posts - the posts created by user
            nickname - secret question 1
            city - secret question 2
            teacher - secret question 3
    """

    userId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default='Normal')
    nickname = db.Column(db.Text(), nullable=False)
    city = db.Column(db.Text(), nullable=False)
    teacher = db.Column(db.Text(), nullable=False)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow())
    updatedAt= db.Column(db.DateTime(), onupdate=datetime.utcnow())
    posts = db.relationship('Posts', backref='users',lazy='dynamic')
    comments = db.relationship('Comments', backref='users',lazy='dynamic')
    replies = db.relationship('Replies', backref='users',lazy='dynamic')

    def __repr__(self) -> str:
        return "<User {}>".format(self.username)


class Posts(db.Model):
    """
        model class for post table
        Attributes:
            id - post id
            userId - the user who created the post
            title - title for post
            description - the description for the post
            body - the main body(content) of the post
            created_at -  the time the post created
            published_at - the time the post published
            likes - the number of likes the post have
            category - the post category
            tags - the tags of the post
    """

    postId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId') )
    title = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text(), nullable=False, unique=False)
    body = db.Column(db.Text(), nullable=False)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow())
    updatedAt= db.Column(db.DateTime(), onupdate=datetime.utcnow())
    likes = db.Column(db.Integer(), default=0)
    category = db.Column(db.String(80), nullable=False)
    comments = db.relationship('Comments', backref='posts', lazy='dynamic')
    replies = db.relationship('Replies', backref='posts', lazy='dynamic')

    

    def __repr__(self) -> str:
        return "<Post {}>".format(self.title)


class Comments(db.Model):
    """
        model class for comments on posts
            Attributes:
                commentId - id for comment
                postId  - post id for the comment
                userId - id for user who wrote the comment
                body - the body(content) of the comment
                createdAt - the time the comment is made
    """
    commentId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer(), db.ForeignKey('users.userId'))
    body = db.Column(db.Text(), nullable=False)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow())
    updatedAt= db.Column(db.DateTime(), onupdate=datetime.utcnow())
    postId = db.Column(db.Integer(), db.ForeignKey('posts.postId'))
    replies = db.relationship('Replies', backref='comments', lazy='dynamic')

    def __repr__(self) -> str:
        return "<Comment {}>".format(self.commentId)

class Replies(db.Model):
    """
        model class for replies on posts
            Attributes:
                replyId - Id of reply
                postId - post id for the reply
                commentId - comment id for the reply
                body - content of the reply
    """
    replyId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer(), db.ForeignKey('users.userId'))
    commentId = db.Column(db.ForeignKey('comments.commentId'))
    postId = db.Column(db.ForeignKey('posts.postId'))
    body = db.Column(db.Text(), nullable=False)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self) -> str:
        return "<Reply {}>".format(self.replyId)

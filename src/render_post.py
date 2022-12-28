"""
Respond for request from posts
"""

from flask import Blueprint, jsonify, request
from .database import db, Posts, Users, Comments, Replies
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime
from json import dumps


def time_formatter(createdtime):
    timenow = datetime.utcnow()
    time_difference = timenow - createdtime

    # Build a string representing the time difference, only including non-zero components
    time_string = ""
    if time_difference.days > 0:
        time_string += f"{time_difference.days} days, "
    if time_difference.seconds // 3600 > 0:
        time_string += f"{time_difference.seconds // 3600} hours, "
    if time_difference.seconds // 60 % 60 > 0:
        time_string += f"{time_difference.seconds // 60 % 60} minutes, "
    if time_difference.seconds % 60 > 0:
        time_string += f"{time_difference.seconds % 60} seconds"

    # Remove the final ", " if it exists
    if time_string.endswith(", "):
        time_string = time_string[:-2]
    

    return "{} ago".format(time_string.split(',')[0])


# Create a blueprint for handle route
renderPost = Blueprint("handle", __name__, url_prefix="/api/v1")

# Recent posts handler
@renderPost.route("/recent")
def recent():
    """
    return recent posts from all available topics
    """
    
    recent_all= {}
    topics = ["Thermodynamics", "Chemistry", "Biotechnology",
              "Reaction Engineering", "Material Engineering",
              "Fluid Mechanics"
             ]
    
    # Retreive data from database 
    for topic in topics:
        post = Posts.query.filter_by(category=topic).order_by(Posts.createdAt.desc()).first()
        about = {}
        about['title'] = post.title
        about['postId'] = post.postId 
        about['description'] = post.description
        createdAt = post.createdAt
        about['duration'] = time_formatter(createdAt)

        # Add to the bigger dictionary
        recent_all[topic] = about

    return jsonify({"msg":recent_all}), 200


# Get post by category
@renderPost.route('/available')
def available():
    """Return available topics.

    Returns:
        dict: A dictionary containing the available topics and their corresponding posts.
    """


    topics = ["Thermodynamics", "Chemistry", "Biotechnology",
              "Reaction Engineering", "Material Engineering",
              "Fluid Mechanics"
             ]
    available = {}

    for topic in topics:
        subject = {}
        posts = Posts.query.filter_by(category=topic).all()
        for post in posts:
            data = {}
            data['title'] = post.title
            data['description'] = post.description
            data['post_id'] = post.postId 
            
            subject[post.postId] = data 
        available[topic] = subject
    
    return jsonify({"msg": available})

@renderPost.route('/post/<int:id>')
def single_post(id):
    """
    This function retrieves information about a single post, including the post itself,
    the user who created the post, and all comments and replies on the post.
    """

    # Retrieve the post with the given id
    post = Posts.query.filter_by(postId=id).first()

    # Retrieve the user who created the post
    user_id = post.userId
    creator = Users.query.filter_by(userId=user_id).first()

    # Retrieve all comments on the post
    comments = Comments.query.filter_by(postId=id).all()

    # Initialize a dictionary to hold the information to be returned
    data = {}
    post_info = {}
    user_info = {}
    comments_info = {}

    # Add information about the post to the dictionary
    post_info['id'] = post.postId
    post_info['title'] = post.title
    post_info['body'] = post.body
    post_info['likes'] = post.likes
    post_info['description'] = post.description
    post_info['duration'] = time_formatter(post.createdAt)

    # Add information about the user who created the post to the dictionary
    user_info['username'] = creator.username
    user_info['number_of_posts'] = len(creator.posts.all())

    # Iterate through the comments and add information about each comment and its replies to the dictionary
    for comment in comments:
        comment_info = {}
        reply_info = {}
        user_id = comment.userId
        comment_info['user'] = Users.query.filter_by(userId=user_id).first().username

        # Retrieve all replies to the current comment
        replies = Replies.query.filter_by(commentId=comment.commentId).all()
        for rep in replies:
            reply = {}
            reply['body'] = rep.body
            reply['user'] = Users.query.filter_by(userId=rep.userId).first().username
            # reply['duration'] = time_formatter(rep.createdAt)

            reply_info[rep.replyId] = reply

        # Add information about the current comment and its replies to the dictionary
        comment_info['replies'] = reply_info
        comment_info['body'] = comment.body
        comment_info['duration'] = time_formatter(comment.createdAt)

        comments_info[comment.commentId] = comment_info

    # Add the dictionaries with information about the post, user, and comments to the data dictionary
    data['post_info'] = post_info
    data['user_info'] = user_info
    data['comment_info'] = comments_info
    return jsonify({"msg": data})


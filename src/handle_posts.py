"""
Handles user actions on post
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import db,Users, Posts, Replies, Comments


userActions = Blueprint('useraction', __name__, url_prefix='/api/v1/handle')


@userActions.route('/likes/<int:postId>', methods=['POST'])
def handleLikes(postId):
    """
    Handles user action on posts
    """
    try:
        # Get the JSON data from the request
        user_input = request.get_json()

        # Check if the request has valid JSON data
        if not user_input:
            return jsonify({"msg": "Not valid JSON"}), 400

        # Check if the request has empty data
        if len(user_input) == 0:
            return jsonify({"msg": "No Data sent"}), 400

        # Check if the request has the required 'data' key
        if "data" not in user_input.keys():
            return jsonify({"msg": "data key not found"}), 400

        # Check if the value of the 'data' key is valid
        if "data" in user_input.keys() and user_input["data"] not in ["like", "dislike"]:
            return jsonify({"msg": "Invalid data value"}), 400

        # Get the post with the specified post_id
        post = Posts.query.filter_by(postId=postId).first()
        # Return a 404 error if the post is not found
        if post is None:
            return jsonify({"msg": "Post not found"}), 404

        # Store the current number of likes for the post
        likes = post.likes

        # Increment or decrement the number of likes based on the value of 'data'
        if user_input["data"] == 'like':
            post.likes += 1
             # Commit the changes to the database
            db.session.commit()
        elif user_input["data"] == 'dislike':
            post.likes -= 1
             # Commit the changes to the database
            db.session.commit()
        else:
            return jsonify({"msg": "unknown data"}), 400

        # Return a success message with the updated number of likes
        return jsonify({"msg": f"{user_input['data']} successfully added"}), 200
    except Exception as e:
        # Return a 500 error if an exception occurs
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


@userActions.route('/comment/<int:postId>', methods=["POST"])
@jwt_required()
def handleComment(postId: int) -> dict:
    """
    This function handles the creation of a new comment for a given post.
    
    Parameters:
        postId (int): The ID of the post to which the comment will be added.
    
    Returns:
        A dictionary containing a message indicating the result of the operation.
        If the comment was created successfully, the dictionary will contain a "msg" field with a value of "Comment created successfully".
        If an error occurred, the dictionary will contain an "error" field with a value indicating the error that occurred.
    """
    # Validate the postId parameter
    if not isinstance(postId, int):
        return {"error": "Invalid postId parameter"}, 400
    
    # Fetch the post from the database
    post = Posts.query.filter_by(postId=postId).first()
    
    # Return an error message if the post does not exist
    if post is None:
        return {"error": "Post not found"}, 404
    
    # Parse the request body as JSON
    user_input = request.get_json()
    
    # Return an error message if the request body is not a valid JSON object
    if not user_input:
        return {"error": "Invalid JSON in request body"}, 400
    
    # Check that the required fields are present in the request body
    if "body" not in user_input.keys():
        return {"error": "Missing body field in request body"}, 400
    
    # Check that the user with the given userId exists
    user = Users.query.filter_by(userId=get_jwt_identity()).first()
    if user is None:
        return {"error": "User with given userId does not exist"}, 400
    
    # Create a new Comment object
    comment = Comments(postId=postId, body=user_input['body'], userId=get_jwt_identity())
    
    # Add the comment to the database and commit the changes
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        # Return an error message if the database operation fails
        return {"error": "Failed to create comment: {}".format(e)}, 500
    
    # Return a success message
    return {"msg": "Comment created successfully"}


@userActions.route('/edit/comment/<int:postId>', methods=["POST"])
def editComment(postId):
    """
    Edit a comment on a post.
    
    Parameters:
    - postId (int): The ID of the post that the comment belongs to.
    
    Returns:
    - A JSON object containing a message indicating the status of the operation. If the operation was successful, the message will be "Comment Updated Sucessfully". If an error occurs, the message will describe the error that occurred.
    
    """
    # Check if the post exists
    post = Posts.query.filter_by(postId=postId).first()
    if post is None:
        return jsonify({"msg":"Post Not Found"}), 404
    
    # Check if the request body is a valid JSON object
    user_input = request.get_json()
    if not user_input:
        return jsonify({"msg":"Not a valid JSON"}), 400
    
    # Check if all required fields are present in the request data
    required = ["commentId","body"]
    for r in required:
        if r not in user_input.keys():
            return jsonify({"msg":"Missing {}".format(r)}), 400
    
    # Check if the comment exists
    comment = Comments.query.filter_by(commentId=user_input['commentId']).first()
    if comment is None:
        return jsonify({"msg":"Comment Not Found"}), 404
    
    # Check if the user has permission to edit the comment
    if comment.userId != get_jwt_identity():
        return jsonify({"msg":"You're not an author of the comment"}), 403
    
    # Update the comment
    try:
        comment.body = user_input["body"]
        db.session.commit()
    except Exception as e:
        return  jsonify({"msg":e}), 500
    
    # Return a success message
    return jsonify({"msg":"Comment Updated Sucessfully"})

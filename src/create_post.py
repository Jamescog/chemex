"""
Handles the creation of post(tutorial)
"""

from flask import Blueprint, jsonify, request
from database import db, Posts, Users, Comments, Replies
from flask_jwt_extended import get_jwt_identity, jwt_required
import uuid
import re
import os
import subprocess
from bs4 import BeautifulSoup

# Create a blueprint for the create route
createPost = Blueprint("create", __name__, url_prefix="/api/v1")


@createPost.route("/create", methods=["POST"])
@jwt_required()
def create():
    """Create new post
        
        Returns:
                the response of the server.
    """
    # Get form data
    file = request.files['file']
    category = request.form['category']
    title = request.form['title']
    description = request.form['description']
    # Validate form data
    if file.filename == '':
        return 'No file selected'
    if not category:
        return 'No category provided'
    if not title:
        return 'No title provided'
    if not description:
        return 'No description provided'

    userId= get_jwt_identity()
    if Users.query.filter_by(userId=userId).first() is None:
        return jsonify({"msg":"No user Found"}), 400

    # Save the file to a temporary location
    file.save('temp.docx')

    # Define the html variable before the try block
    html = ""
    postno = len(Posts.query.all()) + 1
    # Convert the MS Word document to HTML and extract and rename images from it
    try:
        result = subprocess.run(
            ['pandoc', '-s', 'temp.docx', '-t', 'html', '--extract-media=./front-end/images/{}'.format(postno)],
            capture_output=True, text=True, check=True
        )
        html = result.stdout
        os.remove("temp.docx")
    except subprocess.CalledProcessError as e:
        return jsonify({"msg":"Error converting Word document to HTML: {}".format(e)}), 500

    # Update image names in the HTML document
    # Find the src attributes of the images in the HTML content
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img')

    # Update the src attributes with the new path
    for image in images:
        name = image['src'].split("/")[-1]
        image['src'] = 'images/{}/media/{}'.format(postno, name)

    # Convert the BeautifulSoup object back to HTML
    html = str(soup)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    for element in soup.find_all():
        if element.name in ['script', 'iframe', 'base', 'form', 'object']:
            element.decompose()
    body = str(soup.body)
    
    try:
        post  = Posts(userId=userId, body=body, title=title, category=category, description=description)
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg":"Error saving post to database"}), 400
    return jsonify({"msg":"Post created successfully!"}), 201

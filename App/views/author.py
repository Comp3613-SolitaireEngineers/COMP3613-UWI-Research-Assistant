from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from.index import index_views
from App.controllers import *

author_views = Blueprint('author_views', __name__, template_folder='../templates')

@author_views.route('/api/authors', methods=['GET'])
def get_authors_api():
    authors = get_all_authors_json()  # Implement a function to get all publications
    if not authors:
        return jsonify({'message': 'No Authors found'}), 404

    return jsonify(authors), 200

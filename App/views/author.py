from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from.index import index_views
from App.controllers import *

author_views = Blueprint('author_views', __name__, template_folder='../templates')

@author_views.route('/author/publications/<int:author_id>', methods=['GET'])
def get_publications_by_author_api(author_id):
    author = get_author(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404

    return jsonify(get_publications_by_author(author_id))
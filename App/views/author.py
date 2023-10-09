from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from.index import index_views
from App.controllers import *

author_views = Blueprint('author_views', __name__, template_folder='../templates')

@author_views.route('/api/author', methods=['POST'])
@admin_required
def api_create_author():
    data = request.json

    admin_id = data.get('admin_id')
    uwi_id = data.get('uwi_id')
    title = data.get('title')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')

    if None in (admin_id, uwi_id, title, first_name, last_name, password):
        return jsonify({'error': 'Missing data in the request'}), 400

    if not (get_admin(admin_id)):
        return jsonify({'error': 'Admin not found'}), 404

    author = create_author(admin_id, uwi_id, title, first_name, last_name, password)

    if author:
        return jsonify({'message': 'Author created successfully'}), 201
    else:
        return jsonify({'error': 'Author not created'}), 400

@author_views.route('/api/authors', methods=['GET'])
def get_authors_api():
    authors = get_all_authors_json()  # Implement a function to get all publications
    if not authors:
        return jsonify({'message': 'No Authors found'}), 404

    return jsonify(authors), 200


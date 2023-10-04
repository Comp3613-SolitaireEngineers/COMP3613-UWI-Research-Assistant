from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
# from flask_jwt_extended import jwt_required, current_user as jwt_current_user
# from flask_login import current_user, login_required

from.index import index_views

from App.controllers import *
from datetime import datetime  

publication_views = Blueprint('publication_views', __name__, template_folder='../templates')

@publication_views.route('/api/publication', methods=['POST'])
# @admin_required
def create_publication_endpoint():
    data = request.json
    
    result = create_publication(data['admin_id'], data['ISBN'], data['title'], data['publication_date'], data['author_ids'])
    # result = create_publication(data['title'], data['publication_date'], data['author_ids'])

    if result:
        return jsonify({'message': f"Publication '{data['title']}'created with id {result.publication_id}"}), 201

    return jsonify({"error": f"Publication '{data['title']}' not created"}), 500
  

@publication_views.route('/api/publications/<search_term>', methods=['GET'])
def search_publications_api(search_term):
    publication_results, author_results = search_publications(search_term)

    all_results = publication_results + author_results  # Use the + operator to combine lists

    if not all_results:
        return jsonify({'message': 'No results found'}), 404

    results_json = [item.get_json() for item in all_results]

    return jsonify(results_json), 200


def get_all_publications():
    return Publication.query.all()

@publication_views.route('/api/publication_tree/<author_id>', methods=['GET'])
def get_publication_tree_api(author_id):
    author = get_author(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404

    return jsonify(get_publication_tree(author_id)), 200

@publication_views.route('/api/author_publications/<author_id>', methods=['GET'])
def get_publications_by_author_api(author_id):
    # data = request.json
    author = get_author(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404

    return jsonify(get_publications_by_author(author_id)), 200

@publication_views.route('/api/publications', methods=['GET'])
def get_publications_api():
    publications = get_all_publications()  # Implement a function to get all publications
    if not publications:
        return jsonify({'message': 'No Publications found'}), 404

    return jsonify(publications), 200
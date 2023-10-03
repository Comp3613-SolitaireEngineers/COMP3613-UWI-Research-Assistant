from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
# from flask_jwt_extended import jwt_required, current_user as jwt_current_user
# from flask_login import current_user, login_required

from.index import index_views

from App.controllers import *
    

publication_views = Blueprint('publication_views', __name__, template_folder='../templates')

@publication_views.route('/api/publications', methods=['POST'])
def create_publication_endpoint():
    data = request.json
    result = create_publication(data['title'], data['publication_date'], data['author_ids'])

    if result:
        return jsonify({'message': f"Publication  '{data['title']}'created with id {result.id}"}), 201


    return jsonify({"error": f"Publication '{data['title']}' not created"}), 500

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

from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
# from flask_jwt_extended import jwt_required, current_user as jwt_current_user
# from flask_login import current_user, login_required

from.index import index_views

from App.controllers import *
from datetime import datetime  

publication_views = Blueprint('publication_views', __name__, template_folder='../templates')

@publication_views.route('/api/publication', methods=['POST'])
def api_create_publication():
    data = request.json

    author_ids = list(data.get('author_ids'))

    if None in (data['admin_id'], data['isbn'], data['title'], data['publication_date'], author_ids):
        return jsonify({'error': 'Missing data in the request'}), 400

    admin = get_admin(data['admin_id'])
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404

    publication = create_publication(data['admin_id'], data['isbn'], data['title'], data['publication_date'], author_ids)

    if publication:
        return jsonify({'message': f"Publication '{publication_date}' succuessfully created with id {publication.publication_id} "}), 201
    else:
        return jsonify({'error': 'Publication already exists'}), 400

@publication_views.route('/api/author_publications/<author_id>', methods=['GET'])
def api_get_publications_by_author(author_id):

    author = get_author(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    
    author_publications = get_publications_by_author(author_id)

    author_info = {
        'author_id': author.uwi_id,
        'name': f"{author.title} {author.first_name} {author.last_name}",
    }

    if author_publications:
        publications = [{'ISBN': pub.isbn, 'title': pub.title, 'publication_date': pub.publication_date.strftime("%Y/%m/%d")} for pub in author_publications]
        author_info['publications'] = publications
    else:
        author_info['publications'] = 'No Publications.'

    return jsonify([author_info]), 200

@publication_views.route('/api/publication_tree/<author_id>', methods=['GET'])
def api_get_publication_tree(author_id):
    author = get_author(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    return jsonify(get_publication_tree(author_id)), 200


@publication_views.route('/api/publications', methods=['GET'])
def get_publications_api():
    publications = get_all_publications()  # Implement a function to get all publications
    if not publications:
        return jsonify({'message': 'No Publications found'}), 404

    return jsonify(publications), 200

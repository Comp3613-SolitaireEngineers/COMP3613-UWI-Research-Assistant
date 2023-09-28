from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
# from flask_jwt_extended import jwt_required, current_user as jwt_current_user
# from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_publication,
)

publication_views = Blueprint('publication_views', __name__, template_folder='../templates')

@publication_views.route('/publications', methods=['POST'])
def create_publication_endpoint():
    data = request.form
    result = create_publication(data['title'], data['publication_date'], data['author_ids'])
    return jsonify({'message': f"publication {data['title']} created"})

    if result:
        return jsonify({'message': f"Publication {data['title']} created with id {result.id}"}), 201
    return jsonify({"error": f"Publication {data['title']} not created"}), 500
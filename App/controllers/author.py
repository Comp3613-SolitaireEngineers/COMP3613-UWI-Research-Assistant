from App.models import Admin, RegularUser, Author
from App.database import db

def get_author(author_id):
    return Author.query.filter_by(uwi_id = author_id).first()
  
def create_author(admin_id, uwi_id, title, first_name, last_name, password):
    admin = Admin.query.filter_by(admin_id = admin_id).first()
    if admin:
        return admin.create_author(uwi_id, title, first_name, last_name, password)
    return None

def get_all_authors_json():
    authors = Author.query.all()
    if not authors:
        return []
    authors = [author.get_json() for author in authors]
    return authors

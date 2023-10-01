from App.models import Publication, AuthorPublication, Author, Admin
from App.database import db
from sqlalchemy import or_


# this one for author controller
def get_author(author_id):
    return Author.query.get(author_id)

def create_publication(admin_id, title, publication_date, author_ids):
    admin = Admin.query.filter_by(admin_id = admin_id).first()

    if admin:
        return admin.create_publication(title, publication_date, author_ids)
    return None

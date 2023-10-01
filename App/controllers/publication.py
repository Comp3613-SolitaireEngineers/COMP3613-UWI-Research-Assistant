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

def search_publications(search_term):
    publication_results = None
    author_results = None

    if search_term!="":
          publication_results = Publication.query.filter(
                or_(Publication.title.ilike(f'%{search_term}%'), Publication.publication_date.ilike(f'%{search_term}%'))
          ).all()

          author_results = Author.query.filter(
               or_(Author.first_name.ilike(f'%{search_term}%'), Author.last_name.ilike(f'%{search_term}%'))
          ).all()

    else:
        publication_results = Publication.query.all()
        author_results = Author.query.all()

    return publication_results, author_results

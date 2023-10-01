from App.models import Admin, RegularUser, Author
from App.database import db

def get_author(author_id):
    return Author.query.filter_by(uwi_id = author_id).first()

def get_publications_by_author(author_id):
    author = get_author(author_id)
    
    if not author:
        return None

    author_info = {
        'author_id': author.uwi_id,
        'Name': f"{author.title} {author.first_name} {author.last_name}",
    }

    if author.publications:
        publications = [{'title': pub.title, 'publication_date': pub.publication_date} for pub in author.publications]
        author_info['Publications'] = publications
    else:
        author_info['Publications'] = 'No Publications.'

    return [author_info]
  
def create_author(admin_id, uwi_id, title, first_name, last_name, password):
    admin = Admin.query.filter_by(admin_id = admin_id).first()
    print(admin)
    if admin:
        return admin.create_author(uwi_id, title, first_name, last_name, password)
    return None

def get_all_authors_json():
    authors = Author.query.all()
    if not authors:
        return []
    authors = [author.get_json() for author in authors]
    return authors

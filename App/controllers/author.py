from App.models import Author
from App.database import db

def get_author(author_id):
    return Author.query.get(author_id)

def get_publications_by_author(author_id):
    author = get_author(author_id)
    
    if not author:
        return None

    author_info = {
        'author_id': author.author_id,
        'Name': f"{author.title} {author.first_name} {author.last_name}",
    }

    if author.publications:
        publications = [{'title': pub.title, 'publication_date': pub.publication_date} for pub in author.publications]
        author_info['Publications'] = publications
    else:
        author_info['Publications'] = 'No Publications.'

    return [author_info]

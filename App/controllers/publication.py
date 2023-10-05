from App.models import Publication, AuthorPublication, Author, Admin
from .author import get_author
from App.database import db
from sqlalchemy import or_



def create_publication(admin_id, isbn, title, publication_date, author_ids):
    admin = Admin.query.filter_by(admin_id = admin_id).first()

    if admin:
        return admin.create_publication(isbn, title, publication_date, author_ids)
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

    return [publication.get_json() for publication in publication_results], [author.get_json() for author in author_results]


def get_publications_by_author(author_id):
    author = get_author(author_id)
    
    if not author:
        return None

    if author.publications:
       return author.publications

    return None

def get_publication_tree(author_id):
    author = get_author(author_id)
    
    if not author:
        return None

    def get_coauthors(author):
        coauthors = set()
        for publication in author.publications:
            for coauthor in publication.authors:
                if coauthor != author:
                    coauthors.add(coauthor)
        return list(coauthors)
   
    def build_tree(author, visited=set()):
        
        author_id = author.uwi_id
        if author_id in visited:
            return None  # Skip authors that have already been visited

        visited.add(author_id)

        coauthors = get_coauthors(author)
        tree = {
            'author_id': author.uwi_id,
            'name': f"{author.title} {author.first_name} {author.last_name}",
            'publications': [{'ISBN': pub.isbn, 'title': pub.title, 'publication_date': pub.publication_date.strftime("%Y/%m/%d")} for pub in author.publications]
        }

        if coauthors:
            tree['coauthors'] = [build_tree(coauthor, visited=visited) for coauthor in coauthors]
        
        return tree

    publication_tree = build_tree(author)
    return [{'publication_tree': publication_tree}]

def get_all_publications():
    publications = Publication.query.all()
    
    results = [publication.get_json() for publication in publications]
    return results
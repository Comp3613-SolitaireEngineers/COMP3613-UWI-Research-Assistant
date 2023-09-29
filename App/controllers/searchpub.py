from App.models import Author
from App.models import publication
from App.database import db

def search_publications(self,search_term):
    publication_results = None
    author_results = None
    
    if search_term!="":
          publication_results = publication.query.filter(
                or_(publication.title.ilike(f'%{search_term}%'), publication.publication_date.ilike(f'%{search_term}%'))
          ).all()

          author_results = Author.query.filter(
               or_(Author.first_name.ilike(f'%{search_term}%'), Author.last_name.ilike(f'%{search_term}%'))
          ).all()
  
    else:
        publication_results = publication.query.all()
        author_results = Author.query.all()
      
    return publication_results, author_results
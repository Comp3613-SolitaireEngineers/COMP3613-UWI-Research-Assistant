from App.models import Author
from App.models import Publication
from App.database import db

def search_publications(self,search_term):
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
        return "Error: No search term inserted"
      
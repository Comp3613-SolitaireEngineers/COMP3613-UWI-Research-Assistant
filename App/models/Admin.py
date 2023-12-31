from App.database import db
from App.models import User
from .Author import Author
from .Author_Publication import AuthorPublication
from .Publication import Publication

class Admin(User):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(1200), nullable = False,unique=True)

    def __init__(self, admin_id, username, password):
        super().__init__(username, password)
        self.admin_id = admin_id

    def get_json(self):
        return{
            'id': self.id,
            'admin_id' : self.admin_id,
            'username': self.username,
            'role' : 'admin'
        }

    def create_author(self, uwi_id, title, first_name, last_name, password):
        try:
            newAuthor = Author(
                uwi_id = uwi_id,
                title = title,
                first_name = first_name,
                last_name = last_name,
                password = password                
            )
            db.session.add(newAuthor)
            db.session.commit()
            return newAuthor       
        except Exception as e:
            print('Error creating Author: ', e)
            db.session.rollback()
            return None

    def create_author_publication(self, author_ids, publication_id):  
        if not publication_id: 
            return None
        
        if not author_ids:
            return None
        
        try:
            # create a list of AuthorPublication objects
            author_pubs = [AuthorPublication(author_id=author.uwi_id, publication_id=publication_id) for author_id in author_ids for author in (Author.query.filter_by(uwi_id=author_id).first(),) if author]
            for i in author_pubs:
                db.session.add(i)
                
            db.session.commit()
            return author_pubs
        except Exception as e:
            # log the error
            print(e)
            return None 

    def create_publication(self, isbn, title, publication_date, author_ids):
        try:
            # create a new publication object with the given title and publication_date
            new_publication = Publication(isbn=isbn ,title=title, publication_date=publication_date)
            
            # add the publication object to the database session
            db.session.add(new_publication)

            # flush the changes to the database session
            db.session.flush() 
            # create the author_publication objects with the given author_ids and publication_id
            authors = self.create_author_publication(author_ids, new_publication.publication_id)
 
            for author_id in author_ids:
                # get the author object by uwi_id
                author = Author.query.filter_by(uwi_id = author_id).first()
                if author:
                    # check if the author is already in the publication's authors
                    if author not in new_publication.authors:
                        # add the author to the publication's authors
                        author.publications.append(new_publication)
                        new_publication.authors.append(author)
             
            # commit the changes to the database
            db.session.commit() 
            return new_publication
                
        except Exception as e:
            db.session.rollback()
            print(e)
            return None
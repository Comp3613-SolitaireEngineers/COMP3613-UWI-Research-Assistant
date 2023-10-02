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
        
    import logging

    def create_author_publication(self, author_ids, publication_id):  
        if not publication_id: 
            return None
        
        if not author_ids:
            return None
        
        try:
            # create a list of AuthorPublication objects
            author_pubs = [AuthorPublication(author_id=author.uwi_id, publication_id=publication_id) for author_id in author_ids if (author := Author.query.filter_by(uwi_id=author_id).first())]
            for i in author_pubs:
                db.session.add(i)
                
            db.session.commit()
            return author_pubs
        except Exception as e:
            # log the error
            print(e)
            return None

        
    # def create_publication(self, title, publication_date, author_ids):
    #     try:
    #         valid_author_ids = [author_id for author_id in author_ids if Author.query.filter_by(uwi_id=author_id).first()]
            
    #         if len(valid_author_ids) != len(author_ids):
    #             # There is atleast one invalid author in the list
    #             return False
    #         else:
    #             # All authors in author_ids are valid
    #             new_publication = Publication(title=title, publication_date=publication_date)
    #             author_pubs = self.create_author_publication(author_ids=author_ids, publication_id=new_publication.publication_id)
    #             db.session.add(new_publication)
    #             db.session.commit() # https://stackoverflow.com/questions/19388555/sqlalchemy-session-add-return-value

    #             # print(new_publication.id)

    #             return new_publication
            
    #     except Exception as e:
    #         print(e)
    #         return None
    

    def create_publication(self, isbn, title, publication_date, author_ids):
        try:
            # create a new publication object with the given title and publication_date
            new_publication = Publication(isbn=isbn ,title=title, publication_date=publication_date)
            
            # add the publication object to the database session
            db.session.add(new_publication)

            # flush the changes to the database session
            db.session.flush() 

            # get the publication_id of the publication object
            # print(new_publication.publication_id)

            # create the author_publication objects with the given author_ids and publication_id
            authors = self.create_author_publication(author_ids, new_publication.publication_id)

            for author_id in author_ids:
                # get the author object by uwi_id
                author = Author.query.filter_by(uwi_id = author_id).first()
                print(author)
                if author:
                    # check if the author is already in the publication's authors
                    if author not in new_publication.authors:
                        # add the author to the publication's authors
                        author.append(new_publication)
                        new_publication.authors.append(author)
             
            # commit the changes to the database
            db.session.commit() 
            return new_publication
                
        except Exception as e:
            print(e)
            return None
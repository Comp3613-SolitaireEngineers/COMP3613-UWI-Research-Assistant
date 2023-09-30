from App.database import db
from App.models import User
from .Author import Author
from .Author_Publication import AuthorPublication
from .publication import Publication

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
        try:
            for author_id in author_ids:
                print(author_id)
                author = Author.query.filter_by(uwi_id = author_id).first()
                new_author_pub = AuthorPublication(author_id=author.uwi_id, publication_id=publication_id)
                db.session.add(new_author_pub)
                
            db.session.commit()
            return new_author_pub
        except Exception as e:
            print("HI")
            print(e)
            return None
        
    def create_publication(self, title, publication_date, author_ids):
        try:
            print("JI")
            new_publication = Publication(title=title, publication_date=publication_date)
            db.session.add(new_publication)
            db.session.commit() # https://stackoverflow.com/questions/19388555/sqlalchemy-session-add-return-value

            # print(new_publication.id)
            author_pub = self.create_author_publication(author_ids=author_ids, publication_id=new_publication.publication_id)

            return new_publication
            
        except Exception as e:
            print(e)
            return None

    
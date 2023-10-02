from App.database import db
from .User import User

class Author(User):
    __tablename__ = 'author'    
    uwi_id = db.Column(db.String(100), nullable=False, unique=True)
    title = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)    
    publications = db.relationship('Publication', secondary='author_publication', overlaps='authors', lazy=True)

    def __init__(self, uwi_id, title, first_name, last_name, password):
        super().__init__(uwi_id, password)
        self.uwi_id = uwi_id
        self.title = title
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):       
        return f"<Author {self.uwi_id}, {self.title} {self.first_name} {self.last_name}>"

    def get_json(self):
        return {
            'author_id': self.id,
            'uwi_id': self.uwi_id,
            'title': self.title,
            'first_name': self.first_name,
            'last_name': self.last_name,            
        }

from App.database import db

class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    test2 = db.Column(db.String(100), nullable=False)
    publications = db.relationship('Publication', secondary='author_publication', overlaps='authors', lazy=True)

    def __init__(self, title, first_name, last_name):
        self.title = title
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):       
        return f"<Author {self.author_id}, {self.title}, {self.first_name}, {self.last_name}>"

    def toJSON(self):
        return {
            'author_id': self.author_id,
            'title': self.title,
            'first_name': self.first_name,
            'last_name': self.last_name,            
        }

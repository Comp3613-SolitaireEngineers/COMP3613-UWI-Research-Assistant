from App.database import db

class Publication(db.Model):
    __tablename__ = "publication"
    publication_id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(120), nullable=False, unique=True)
    title = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime, default=None)
    authors = db.relationship('Author', secondary='author_publication', overlaps='publications', lazy=True)

    def __init__(self, isbn, title, publication_date):       
        self.isbn = isbn
        self.title = title
        self.publication_date = publication_date

    def __repr__(self):
        return f'<Publication {self.publication_id}, ISBN: {self.isbn}, title: {self.title}, publication date: {self.publication_date.strftime("%Y/%m/%d")}>'
    
    def toJSON(self):
        return{
            'publication_id': self.publication_id,
            'ISBN': self.isbn,
            'title': self.title,
            'publication_date': self.publication_date.strftime("%Y/%m/%d, %H:%M:%S") if self.publication_date else None
        }
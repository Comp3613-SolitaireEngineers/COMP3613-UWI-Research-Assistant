from App.database import db

class Publication(db.Model):
    __tablename__ = "publication"
    publication_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime, default=None)
    authors = db.relationship('Author', secondary='author_publication', overlaps='publications', lazy=True)

    def __init__(self, title, publication_date):       
        self.title = title
        self.publication_date = publication_date

    def __repr__(self):
        return f'<publication {self.publication_id} title: {self.title} publication date: {self.publication_date}>'
    
    def toJSON(self):
        return{
            'publication_id': self.publication_id,
            'title': self.title,
            'publication_date': self.publication_date.strftime("%Y/%m/%d, %H:%M:%S") if self.publication_date else None
        }
from App.database import db

class AuthorPublication(db.Model):
    __tablename__ = 'author_publication'
    authorpublication_id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.String(120), db.ForeignKey('author.uwi_id')) 
    publication_id = db.Column(db.String(120), db.ForeignKey('publication.publication_id'))  

    def __init__(self, author_id,publication_id):
        self.author_id = author_id
        self.publication_id = publication_id   

    def __repr__(self): 
        return f"<AuthorPublication {self.authorpublication_id}, {self.author_id}, {self.publication_id}>"

    def get_json(self):
        return {
            'authorpublication_id': self.authorpublication_id,
            'author_id': self.author_id,
            'publication_id': self.publication_id,
        }
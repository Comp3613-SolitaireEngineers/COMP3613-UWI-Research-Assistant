from flask_login import UserMixin
from App.database import db

class RegularUser(db.Model, UserMixin):
    __tablename__ = 'regularuser'
    id = db.Column(db.Integer, primary_key=True)


    def __init__(self, username, password):
        super().__init__(username, password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }



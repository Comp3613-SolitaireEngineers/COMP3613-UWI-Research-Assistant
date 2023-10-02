from App.database import db
from App.models import User

class RegularUser(User):
    __tablename__ = 'regularuser'
    id = db.Column(db.String(120), primary_key=True)


    def __init__(self, username, password):
        super().__init__(username, password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }



from App.database import db
from .User import User

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

    def create_author(title, first_name, last_name):
        pass

    
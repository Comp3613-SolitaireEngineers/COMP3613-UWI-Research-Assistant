from App.database import db
from .User import User
from .Author import Author

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
            # print('Error creating Author: ', e)
            db.session.rollback()
            return None

    
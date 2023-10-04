from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
import uuid

def generate_short_uuid():
    return str(uuid.uuid4())[:8]

class User(db.Model, UserMixin):
    __abstract__ = True
    __tablename__ = 'user'
    id = db.Column(db.String(120), primary_key=True, default=generate_short_uuid, server_default='gen_random_uuid()')
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='scrypt')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


from App.models import RegularUser
from App.database import db

def create_user(username, password):
    newuser = RegularUser(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return RegularUser.query.filter_by(username=username).first()

def get_user(id):
    return RegularUser.query.get(id)

def get_all_users():
    return RegularUser.query.all()

def get_all_users_json():
    users = RegularUser.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    
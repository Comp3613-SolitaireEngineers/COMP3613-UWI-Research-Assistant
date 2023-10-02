from App.models import Admin
from App.controllers import is_user_available
from App.database import db

def create_admin(admin_id, username, password):
    if not is_user_available(username):
        return None

    try:   
        admin = Admin(admin_id = admin_id, username=username, password=password)
        db.session.add(admin)
        db.session.commit() 
        return admin
    except Exception as e:        
        print('Error in create admin') 
        # print(e)           
        db.session.rollback()
        return None 

def list_admins():
    return Admin.query.all()

def get_admin_by_username(username):
    return Admin.query.filter_by(username=username).first()

def get_admin(id):
    return Admin.query.filter_by(admin_id = id).first()

def get_all_admins():
    return Admin.query.all()

def get_all_admins_json():
    admins = Admin.query.all()
    if not admins:
        return []
    admins = [admin.get_json() for admin in admins]
    return admins
from App.models import Admin, RegularUser
from App.database import db

def create_author(admin_id, uwi_id, title, first_name, last_name, password):
    admin = Admin.query.get(admin_id)
    
    if admin:
        return admin.create_author(uwi_id, title, first_name, last_name, password)
    return None
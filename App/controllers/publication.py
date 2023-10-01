from App.models import Publication, AuthorPublication, Author, Admin
from App.database import db

# this one for author controller
def get_author(author_id):
    return Author.query.get(author_id)

def create_publication(admin_id, title, publication_date, author_ids):
    admin = Admin.query.filter_by(admin_id = admin_id).first()

    if admin:
        return admin.create_publication(title, publication_date, author_ids)
    return None
   
# def create_author_publication(author_ids, publication_id):
    
#     try:
#         for author_id in author_ids:
#             author = get_author(author_id)
#             new_author_pub = AuthorPublication(author_id=author.id, publication_id=publication_id)
#             db.session.add(new_author_pub)

#         db.session.commit()

#         return new_author_pub
#     except:
#         return None
from App.models import Publication, AuthorPublication
from App.database import db

# this one for author controller
def get_author(author_id):
    return Author.query.get(author_id)

def create_publication(title, publication_date, author_ids):
    new_publication = Publication(title=title, publication_date=publication_date)

    try:
        db.session.add(new_publication)
        db.session.commit() # https://stackoverflow.com/questions/19388555/sqlalchemy-session-add-return-value

        print(new_publication.id)
        author_pub = create_author_publication(author_ids=author_ids, publication_id=new_publication.id)

        return new_publication
        
    except:
        return None


def create_author_publication(author_ids, publication_id):
    
    try:
        for author_id in author_ids:
            author = get_author(author_id)
            new_author_pub = AuthorPublication(author_id=author.id, publication_id=publication_id)
            db.session.add(new_author_pub)

        db.session.commit()

        return new_author_pub
    except:
        return None
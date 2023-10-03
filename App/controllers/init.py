from App.models import Admin
from App.database import db
from .admin import create_admin
from .author import create_author
from .publication import create_publication
from datetime import datetime

def initialise_db():
    admin = create_admin("strid", "admin1", "admin1pass")

    if admin:
        create_author("strid", "1", "Ms", "Hermione", "Granger", "hg1")
        create_author("strid", "2", "Mr", "Harry", "Potter", "hp2")
        create_author("strid", "3", "Mr", "Ron", "Weasley", "rw3")

        publication_date = datetime.now()

        pub1 = create_publication("strid", "123", "paper on AI", publication_date, ["1", "2"])
        pub2 = create_publication("strid", "456", "paper on Planes", publication_date, ["1"])
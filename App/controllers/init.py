from App.models import Admin
from App.database import db
from .admin import create_admin
from .author import create_author
from .publication import create_publication
from datetime import datetime

def initialise_db():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')

    admin = create_admin("strid", "admin1", "admin1pass")

    if admin:
        create_author("strid", "1", "Ms", "Hermione", "Granger", "hg1")
        create_author("strid", "2", "Mr", "Harry", "Potter", "hp2")
        create_author("strid", "3", "Mr", "Ron", "Weasley", "rw3")
        create_author("strid", "4", "Ms", "Luna", "Lovegood", "ll4")
        create_author("strid", "5", "Mr", "Draco", "Malfoy", "dm5")
        create_author("strid", "6", "Ms", "Ginny", "Weasley", "gw6")

        publication_date = datetime.now()

        author_lists = [
            ["1", "2"],
            ["1", "3", "4"],
            ["1", "2", "3", "5"],
            ["1", "4", "6", "2"],
            ["2", "3"],
            ["5"],
            ["1", "3", "6"],
            ["2", "4", "1", "3"],
            ["3", "5", "4"],
            ["4", "6", "1"],
        ]

        create_publication("strid", "pub1", "Paper on Herbology", publication_date, author_lists[0])
        create_publication("strid", "pub2", "Paper on Planes", publication_date, author_lists[1])
        create_publication("strid", "pub3", "Paper on Magic", publication_date, author_lists[2])
        create_publication("strid", "pub4", "Paper on Quidditch", publication_date, author_lists[3])
        create_publication("strid", "pub5", "Paper on Wizards", publication_date, author_lists[4])
        create_publication("strid", "pub6", "Paper on Creatures", publication_date, author_lists[5])
        create_publication("strid", "pub7", "Paper on Potions", publication_date, author_lists[6])
        create_publication("strid", "pub8", "Paper on Spells", publication_date, author_lists[7])
        create_publication("strid", "pub9", "Paper on Hogwarts", publication_date, author_lists[8])
        create_publication("strid", "pub10", "Paper on Dark Arts", publication_date, author_lists[9])

    print('database intialized')
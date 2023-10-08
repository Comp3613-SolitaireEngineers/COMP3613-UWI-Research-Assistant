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
        # create_author("strid", "1", "Ms", "Hermione", "Granger", "hg1")
        # create_author("strid", "2", "Mr", "Harry", "Potter", "hp2")
        # create_author("strid", "3", "Mr", "Ron", "Weasley", "rw3")

        # publication_date = datetime.now()

        # pub1 = create_publication("strid", "pub1", "paper on AI", publication_date, ["1", "2"])
        # pub2 = create_publication("strid", "pub2", "paper on Planes", publication_date, ["1"])
        # pub3 = create_publication("strid", "pub3", "paper on AI", publication_date, ["1", "2"])
        # pub4 = create_publication("strid", "pub4", "paper on Planes", publication_date, ["1"])
        # pub5 = create_publication("strid", "123", "paper on AI", publication_date, ["1", "2"])
        # pub6 = create_publication("strid", "456", "paper on Planes", publication_date, ["1"])


        a = create_author("strid", "1", "Ms", "Hermione", "Granger", "hg1")
        create_author("strid", "2", "Mr", "Harry", "Potter", "hp2")
        create_author("strid", "3", "Mr", "Ron", "Weasley", "rw3")
        create_author("strid", "4", "Ms", "Luna", "Lovegood", "ll4")
        create_author("strid", "5", "Mr", "Draco", "Malfoy", "dm5")
        create_author("strid", "6", "Ms", "Ginny", "Weasley", "gw6")
        # create_author("strid", "7", "Mr", "Neville", "Longbottom", "nl7")
        # create_author("strid", "8", "Ms", "Bellatrix", "Lestrange", "bl8")
        # create_author("strid", "9", "Mr", "Sirius", "Black", "sb9")
        # create_author("strid", "10", "Mr", "Remus", "Lupin", "rl10")

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
            # ["1", "3", "5", "7"],
            # ["2", "4", "6", "8", "10"],
            # ["1", "2", "3", "4", "5", "6", "7"],
            # ["4", "6"],
            # ["1", "2", "3", "5", "8", "10"],
            # ["1", "4", "6", "7"],
            # ["2", "3", "5", "9"],
            # ["1", "2", "4", "6", "7"],
            # ["1", "3", "5", "7", "10"],
            # ["2", "4", "8", "9"],
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
        # create_publication("strid", "pub11", "Paper on Invisibility", publication_date, author_lists[10])
        # create_publication("strid", "pub12", "Paper on Patronus", publication_date, author_lists[11])
        # create_publication("strid", "pub13", "Paper on Horcruxes", publication_date, author_lists[12])
        # create_publication("strid", "pub14", "Paper on Marauders", publication_date, author_lists[13])
        # create_publication("strid", "pub15", "Paper on Phoenix", publication_date, author_lists[14])
        # create_publication("strid", "pub16", "Paper on Time-Turner", publication_date, author_lists[15])
        # create_publication("strid", "pub17", "Paper on Quibbler", publication_date, author_lists[16])
        # create_publication("strid", "pub18", "Paper on Triwizard", publication_date, author_lists[17])
        # create_publication("strid", "pub19", "Paper on Beasts", publication_date, author_lists[18])
        # create_publication("strid", "pub20", "Paper on Potion-Making", publication_date, author_lists[19])

    print('database intialized')
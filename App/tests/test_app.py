import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from unittest import mock

from App.main import create_app
from App.database import db, create_db
from App.models import User, Author, Admin, Publication, AuthorPublication, RegularUser
from App.controllers import (
    create_user,
    login,
    create_author,
    create_publication,
    create_admin,
    search_publications,
    get_publications_by_author,
    get_publication_tree,
    get_all_authors_json,
    get_all_publications
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = RegularUser("bob", "bobpass")
        assert user.username == "bob"

    def test_new_author(self):
        author = Author("817364712", "Mr", "ron", "john", "ronpass")
        assert author.uwi_id == "817364712"
        assert author.title == "Mr"
        assert author.first_name == "ron"
        assert author.last_name == "john"
        
        
    def test_new_admin(self):
        admin = Admin("817630671", "admin1", "admin1pass")
        assert admin.admin_id == "817630671"
        assert admin.username == "admin1"
        

    def test_new_publication(self):
        publication = Publication("978-0-596-52068-7", "Example Paper", "01-02-2023")
        assert publication.isbn == "978-0-596-52068-7"
        assert publication.title == "Example Paper"
        assert publication.publication_date == "01-02-2023"
    
    def test_new_author_publication(self):
        author_pub = AuthorPublication("817364712", "pub4")
        assert author_pub.author_id == "817364712"
        assert author_pub.publication_id == "pub4"


    # pure function no side effects or integrations called
    def test_user_get_json(self):
        user = RegularUser("bob", "bobpass")
        user_json = user.get_json()
        
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})

    def test_author_get_json(self):
        author = Author("817364712", "Mr", "ron", "john", "ronpass")
        author_json = author.get_json()

        self.assertDictEqual(
            author_json, 
            {
                "author_id": None,
                'uwi_id': "817364712",
                'title': "Mr",
                'first_name': "ron",
                'last_name': "john"
            })
        
    def test_admin_get_json(self):
        admin = Admin("817630671", "admin1", "admin1pass")
        admin_json = admin.get_json()

        self.assertDictEqual(
            admin_json,
            {
                'id': None,
                'admin_id' : "817630671",
                'username': "admin1",
                'role' : 'admin'
            })

    def test_publication_get_json(self):
        pub_date = datetime.now()
        publication = Publication("978-0-596-52068-7", "Example Paper", pub_date)
        pub_json = publication.get_json()

        self.assertDictEqual(
            pub_json,
            {
                'publication_id': None,
                'ISBN': "978-0-596-52068-7",
                'title': "Example Paper",
                'publication_date': pub_date.strftime("%Y/%m/%d, %H:%M:%S")
            })
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = RegularUser("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = RegularUser("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    #related to scope
    def test_create_admin_success(self):
        admin = create_admin("strid", "admin1", "admin1pass")
        assert admin.username == "admin1"
        
    def test_create_admin_failure(self):
        admin = create_admin("strid2", "admin2", "admin2pass")
        admin2 = create_admin("strid2", "admin2", "admin2pass")
        assert admin2 == None

    def test_create_author_success(self):
        author = create_author("strid", "1", "Mr.", "rick", "sanchez", "tiny_rick")
        assert author.first_name == "rick"
        
    def test_create_author_failure(self):
        author = create_author("strid3", "2", "Mr.", "rick", "sanchez", "tiny_rick") #Incorrect admin ID
        assert author == None

    def test_create_publication_success(self):
        author1 = create_author("strid", "3", "Mr.", "morty", "sanchez", "evil_morty")
        author2 = create_author("strid", "4", "Ms.", "summer", "smith", "summer_time")
        pub_date = datetime.now()
        publication = create_publication("strid", "pub1", "Paper on Herbology", pub_date, [author1.uwi_id, author2.uwi_id])
        assert publication.title == "Paper on Herbology"
        
    def test_create_publication_failure(self):
        author1 = create_author("strid", "5", "Mr.", "Luis", "Doe", "evil_luis")
        author2 = create_author("strid", "6", "Ms.", "autumn", "gold", "autumn_time")
        pub_date = datetime.now()
        publication1 = create_publication("strid", "pub12", "Paper on Herbology", pub_date, [author1.uwi_id, author2.uwi_id])
        publication2 = create_publication("strid", "pub12", "Paper on Snow", pub_date, [author1.uwi_id, author2.uwi_id])#ISBN Exists. Unique ISBN needed
        assert publication2 == None

    def test_search_publications_by_publication(self):
        author = create_author("strid", "7", "Mr.", "jerry", "smith(cowardice)", "cowardly_jerry")
        pub_date = datetime.now()
        pub_date_formatted = pub_date.strftime("%Y/%m/%d, %H:%M:%S")
        publication = create_publication("strid", "pub2", "Paper on Cowardice", pub_date, [author.uwi_id])
        publications, authors = search_publications("Cowardice")
        self.assertListEqual([{"publication_id": publication.publication_id, "ISBN":"pub2", "title":"Paper on Cowardice", "publication_date":pub_date_formatted}], publications)
        

    def test_search_publications_by_author(self):
        author = create_author("strid", "8", "Mr.", "joe", "john", "johnny")
        pub_date = datetime.now()
        pub_date_formatted = pub_date.strftime("%Y/%m/%d, %H:%M:%S")
        publication = create_publication("strid", "pub14", "Paper on Stories", pub_date, [author.uwi_id])
        publications, authors = search_publications("joe")
        
        self.assertListEqual([{"author_id":author.id, "uwi_id":"8", "title":"Mr.", "first_name":"joe", "last_name":"john"}], authors)
        
    def test_search_publication_no_results_authors(self):
        publications,authors = search_publications("NULL")       
        self.assertFalse(authors)
    
    def test_search_publication_no_results_publications(self):
        publications,authors = search_publications("NULL")       
        self.assertFalse(publications)

    def test_get_publications_by_author_success(self):
        author = create_author("strid", "9", "Ms.", "beth", "smith", "betty")
        pub_date = datetime.now()
        pub_date_formatted = pub_date.strftime("%Y/%m/%d, %H:%M:%S")
        publication = create_publication("strid", "pub3", "Paper on Who is the Clone Beth?", pub_date, ["9", "2"])
        publications = get_publications_by_author("9")
        publications_json = [pub.get_json() for pub in publications]
        
        self.assertListEqual([{"publication_id": publication.publication_id, "ISBN":"pub3", "title":"Paper on Who is the Clone Beth?", "publication_date":pub_date_formatted}], publications_json)

    def test_get_publications_by_author_failure(self):
        publications = get_publications_by_author("NULL")
        
        self.assertFalse(publications)

    def test_get_valid_publication_tree(self):
        author1 = create_author("strid", "11", "Mr.", "bird", "person", "bird_man")
        author2 = create_author("strid", "12", "Ms.", "poopy", "butthole", "poopy")
        author3 = create_author("strid", "13", "Mr.", "rick", "prime", "prime_rick")

        pub_date  = datetime.strptime("29 Sep 2023 10:00", "%d %b %Y %H:%M")

        publication1 = create_publication("strid", "pub4", "Paper on Rick and Morty", pub_date, [author1.uwi_id, author2.uwi_id])
        publication2 = create_publication("strid", "pub5", "Paper on Rick and Morty: The Vat of Acid", pub_date, [author3.uwi_id, author2.uwi_id])

       
        tree1 = get_publication_tree("11")
        expected_tree1= [{'publication_tree': 
                            {'author_id': author1.uwi_id, 
                             'name': 'Mr. bird person', 
                             'publications': [
                                                {
                                                    'ISBN': 'pub4', 
                                                    'title': 'Paper on Rick and Morty', 
                                                    'publication_date': pub_date.strftime("%Y/%m/%d")
                                                }
                                             ], 
                             'coauthors':   [
                                                {
                                                    'author_id': author2.uwi_id, 
                                                    'name': 'Ms. poopy butthole', 
                                                    'publications': [
                                                                        {
                                                                            'ISBN': 'pub4', 
                                                                            'title': 'Paper on Rick and Morty', 
                                                                            'publication_date': pub_date.strftime("%Y/%m/%d")
                                                                        }, 
                                                                        {
                                                                            'ISBN': 'pub5', 
                                                                            'title': 'Paper on Rick and Morty: The Vat of Acid', 
                                                                            'publication_date': pub_date.strftime("%Y/%m/%d")
                                                                        }
                                                                    ], 
                                                    'coauthors':[
                                                                    {
                                                                        'author_id': author1.uwi_id, 
                                                                        'name': 'Mr. bird person', 
                                                                        'publications': [{
                                                                                            'ISBN': 'pub4', 
                                                                                            'title': 'Paper on Rick and Morty', 
                                                                                            'publication_date': pub_date.strftime("%Y/%m/%d")
                                                                                        }]
                                                                    }, 
                                                                    {
                                                                        'author_id': author3.uwi_id, 
                                                                        'name': 'Mr. rick prime', 
                                                                        'publications': [
                                                                                            {
                                                                                                'ISBN': 'pub5', 
                                                                                                'title': 'Paper on Rick and Morty: The Vat of Acid', 
                                                                                                'publication_date': pub_date.strftime("%Y/%m/%d")
                                                                                            }
                                                                                        ], 
                                                                        'coauthors':[
                                                                                        {
                                                                                            'author_id': author2.uwi_id, 
                                                                                            'name': 'Ms. poopy butthole', 
                                                                                            'publications': [
                                                                                                                {
                                                                                                                'ISBN': 'pub4', 
                                                                                                                'title': 'Paper on Rick and Morty', 
                                                                                                                'publication_date': pub_date.strftime("%Y/%m/%d")
                                                                                                                }, 
                                                                                                                {
                                                                                                                'ISBN': 'pub5', 
                                                                                                                'title': 'Paper on Rick and Morty: The Vat of Acid', 
                                                                                                                'publication_date': pub_date.strftime("%Y/%m/%d")
                                                                                                                }
                                                                                                            ]
                                                                                        }
                                                                                    ]
                                                                    }
                                                                ]
                                                }
                                            ]
                             }
                        }]
        self.assertListEqual(expected_tree1, tree1)

    def test_get_invalid_publication_tree(self):
        tree2 = get_publication_tree("None")
        self.assertIsNone(tree2)

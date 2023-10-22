import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    create_author,
    create_publication,
    create_admin,
    search_publications,
    get_publications_by_author,
    get_publication_tree
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    # def test_get_json(self):
    #     user = User("bob", "bobpass")
    #     user_json = user.get_json()
    #     self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
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

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # # Tests data changes in the database
    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"

    #related to scope
    def test_create_admin(self):
        admin = create_admin("strid", "admin1", "admin1pass")
        assert admin.username == "admin1"

    def test_create_author(self):
        author = create_author("strid", "1", "Mr.", "rick", "sanchez", "tiny_rick")
        assert author.first_name == "rick"

    def test_create_publication(self):
        author1 = create_author("strid", "2", "Mr.", "morty", "sanchez", "evil_morty")
        author2 = create_author("strid", "3", "Ms.", "summer", "smith", "summer_time")
        pub_date = datetime.now()
        publication = create_publication("strid", "pub1", "Paper on Herbology", pub_date, [author1.uwi_id, author2.uwi_id])
        assert publication.title == "Paper on Herbology"

    def test_search_publications(self):
        author = create_author("strid", "4", "Mr.", "jerry", "smith(cowardice)", "cowardly_jerry")
        pub_date = datetime.now()
        pub_date_formatted = pub_date.strftime("%Y/%m/%d, %H:%M:%S")
        publication = create_publication("strid", "pub2", "Paper on Cowardice", pub_date, [author.uwi_id])
        publications, authors = search_publications("Cowardice")
        self.assertListEqual([{"publication_id": publication.publication_id, "ISBN":"pub2", "title":"Paper on Cowardice", "publication_date":pub_date_formatted}], publications)
        self.assertListEqual([{"author_id":author.id, "uwi_id":"4", "title":"Mr.", "first_name":"jerry", "last_name":"smith(cowardice)"}], authors)

    def test_get_publications_by_author(self):
        author = create_author("strid", "5", "Ms.", "beth", "smith", "betty")
        pub_date = datetime.now()
        pub_date_formatted = pub_date.strftime("%Y/%m/%d, %H:%M:%S")
        publication = create_publication("strid", "pub3", "Paper on Who is the Clone Beth?", pub_date, ["5", "2"])
        publications = get_publications_by_author("5")
        publications_json = [pub.get_json() for pub in publications]
        
        self.assertListEqual([{"publication_id": publication.publication_id, "ISBN":"pub3", "title":"Paper on Who is the Clone Beth?", "publication_date":pub_date_formatted}], publications_json)

    def test_get_publication_tree(self):
        author1 = create_author("strid", "7", "Mr.", "bird", "person", "bird_man")
        author2 = create_author("strid", "8", "Ms.", "poopy", "butthole", "poopy")
        author3 = create_author("strid", "9", "Mr.", "rick", "prime", "prime_rick")

        pub_date  = datetime.strptime("29 Sep 2023 10:00", "%d %b %Y %H:%M")

        publication1 = create_publication("strid", "pub4", "Paper on Rick and Morty", pub_date, [author1.uwi_id, author2.uwi_id])
        publication2 = create_publication("strid", "pub5", "Paper on Rick and Morty: The Vat of Acid", pub_date, [author3.uwi_id, author2.uwi_id])

       
        tree1 = get_publication_tree("7")
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

        tree2 = get_publication_tree("10")
        self.assertIsNone(tree2)


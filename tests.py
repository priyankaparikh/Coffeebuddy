""" Module to test the CoffeeBuddy application.
"""
import unittest
from server import app
from models import db, example_data, connect_to_db
from yelper import *

#####################################################################

class CoffeshopTests(unittest.TestCase):
    """Tests the Yelp API for correct responses."""

    def setup(self):
        """ Base setup for the Yelp Api. """
        self.client = app.test_client()
        app.config['TESTING'] = True

        def mock_request(host, path, api_key, url_params=None):
            return "[{u'alias': u'coffee', u'title': u'Coffee & Tea'}]"

        requests.request = mock_request

        def mock_search(location):
            return "[{u'alias': u'coffee', u'title': u'Coffee & Tea'}]"

        search = mock_search


        def test_mock_request(self):
            self.assertIn('coffee', result)

        def test_mock_request(self):
            self.assertIn('coffee', result)

class CoffeebuddyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        # Connect to test database
        connect_to_db(app, uri="postgresql:///testdb")
        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """drop the db at the end of every test."""
        # close the session
        db.session.close()
        # drop the db
        db.drop_all()

    def test_home(self):
        result = self.client.get("/")
        self.assertIn('<div class="carousel-caption">', result.data)

    def test_login_page(self):
        result = self.client.get("/login")
        self.assertIn('<div class="form-group">', result.data)

    def test_registration_page(self):
        """ Test register page for information from db."""

        result = self.client.get("/register")
        # Test register page for book_genres from db.
        self.assertIn("Horror", result.data)
        # Test register page for movie_genres from db
        self.assertIn("Action", result.data)
        # Test register page for music_genres from db.
        self.assertIn("Metal", result.data)
        # Test register page for food_habits from db.
        self.assertIn("Vegan", result.data)
        # Test register page for fav_cuisines from db.
        self.assertIn("Italian", result.data)
        # Test register page for hobbies from db.
        self.assertIn("Sewing", result.data)
        # Test register page for political_views from db.
        self.assertIn("Democrat", result.data)
        # Test register page for religions from db.
        self.assertIn("Hindu", result.data)
        # Test register page for outdoor activities from db.
        self.assertIn("hiking", result.data)
        # Test register page HTML
        self.assertIn("<h2>New User Registeration<h2>", result.data)



    # def test_register2(self):
    #     """ Test the registeration process."""
    #     result = self.client.post("/register",
    #                                 data={
    #                                 "fname": "Jane",
    #                                 "lname": "Doe",
    #                                 "email": "jdoe@gmail.com",
    #                                 "user_name": "jdo",
    #                                 "password": "tamtam",
    #                                 "date_of_birth": "26-5-1978",
    #                                 "zipcode": "97678",
    #                                 "phone": "404-995-0900",
    #                                 "one_word": "joke",
    #                                 "Preferred book genre": 1,
    #                                 "Preferred movie genre": 1,
    #                                 "Preferred music genre": 2,
    #                                 "Food habits": 1,
    #                                 "Preferred cuisine type": 2,
    #                                 "Favorite hobby": 1,
    #                                 "Political ideology": 1,
    #                                 "Religious ideology": 1,
    #                                 "Favorite Outdoor activity": 1,
    #                                 "profile_picture": ""},
    #                                 follow_redirects=True)
    #     self.assertIn("<h1>Trip Form</h1>", result.data)

    # def test_plan_trip_page(self):
    #     """ test if the plan trip page loads correctly """
    #
    #     result = self.client.get("/plan_trip")
    #
    #     self.assertIn("<p> What time would you like to get coffee? </p>")
    #
    #
    # def test_plan_trip(self):
    #     """ test the input of user and check for the redirect."""
    #
    #     result = self.client.post("/plan_trip",
    #                             data={
    #                             "triptime": "2018-02-15 22:20:21.313644",
    #                             "pincode": 95111},
    #                             follow_redirects=True)
    #
    #     self.assertIn("<p> Here is a list of your potential Matches</p>",
    #                 result.data)


####################################################################


if __name__ == "__main__":
    unittest.main()

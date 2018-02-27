""" This module tests for
- testing the the routes
- testing if the templates rendered correctly
- testing the db for correct models
- testing if the page got the correct info
    from the db
"""

import unittest
from server import app
from models import db, example_data, connect_to_db

#####################################################################


class CoffeeTests(unittest.TestCase):
    """Tests basic get routes for Coffebuddy Web app site."""

    def setUp(self):
        """ Do this before any test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        result = self.client.get("/")
        self.assertIn("<h1>CoffeeBuddy</h1>", result.data)

    def test_login1(self):
        result = self.client.get("/login")
        self.assertIn("<h1> Login Form</h1>", result.data)


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

    def test_user(self):
        """ Test the user profile page for user_info."""

        result = self.client.get("/user_info")
        self.assertIn("", result.data)

    def test_user_interests(self):
        """ Test the user profile page for user_interests."""

        result = self.client.get("user/info")
        self.assertIn("", result)

    def test_book_genres_list(self):
        """ Test register page for book_genres from db."""

        result = self.client.get("/register")
        self.assertIn("Horror", result.data)

    def test_movie_genres_list(self):
        """ Test register page for movie_genres from db."""

        result = self.client.get("/register")
        self.assertIn("Action", result.data)

    def test_music_genres_list(self):
        """ Test register page for music_genres from db."""

        result = self.client.get("/register")
        self.assertIn("Metal", result.data)

    def test_food_habit_list(self):
        """ Test register page for food_habits from db."""

        result = self.client.get("/register")
        self.assertIn("Vegan", result.data)

    def test_fav_cuisine_list(self):
        """ Test register page for fav_cuisines from db."""

        result = self.client.get("/register")
        self.assertIn("Italian", result.data)

    def test_hobby1(self):
        """ Test register page for hobbies from db."""

        result = self.client.get("/register")
        self.assertIn("Sewing", result.data)

    def test_political_view_list(self):
        """ Test register page for political_views from db."""

        result = self.client.get("/register")
        self.assertIn("Democrat", result.data)

    def test_religion_list(self):
        """ Test register page for religions from db."""

        result = self.client.get("/register")
        self.assertIn("Hindu", result.data)

    def test_outdoor_list(self):
        """ Test register page for outdoor activities from db."""

        result = self.client.get("/register")
        self.assertIn("hiking", result.data)

    def test_login2(self):
        """ Test the the login page for the correct path."""

        result = self.client.post("/login",
                                data={"email": "eforman@gmail.com",
                                    "password": "Whimsical"},
                                follow_redirects=True)
        self.assertIn("<h1>Trip Form</h1>", result.data)

    def test_register1(self):
        """ Test the registeration page."""

        result = self.client.get("/register")
        self.assertIn("<p>User name</p>", result.data)

    def test_register2(self):
        """ Test the registeration process."""
        result = self.client.post("/register",
                                    data={
                                    "fname": "Jane",
                                    "lname": "Doe",
                                    "email": "jdoe@gmail.com",
                                    "user_name": "jdo",
                                    "password": "tamtam",
                                    "date_of_birth": "26-5-1978",
                                    "zipcode": "97678",
                                    "phone": "404-995-0900",
                                    "one_word": "joke",
                                    "Preferred book genre": 1,
                                    "Preferred movie genre": 1,
                                    "Preferred music genre": 2,
                                    "Food habits": 1,
                                    "Preferred cuisine type": 2,
                                    "Favorite hobby": 1,
                                    "Political ideology": 1,
                                    "Religious ideology": 1,
                                    "Favorite Outdoor activity": 1,
                                    "profile_picture": ""},
                                    follow_redirects=True)
        self.assertIn("<h1>Trip Form</h1>", result.data)

    def test_plan_trip_page(Self):
        """ test if the plan trip page loads correctly """

        result = self.client.get("/plan_trip")

        self.assertIn("<p> What time would you like to get coffee? </p>")


    def test_plan_trip(self):
        """ test the input of user and check for the redirect."""

        result = self.client.post("/plan_trip",
                                data={
                                "triptime": "2018-02-15 22:20:21.313644",
                                "pincode": 95111},
                                follow_redirects=True)

        self.assertIn("<p> Here is a list of your potential Matches</p>",
                    result.data)

####################################################################


if __name__ == "__main__":
    unittest.main()

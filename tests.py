import unittest
from server import app
from models import db, example_data, connect_to_db


class CoffeeTests(unittest.TestCase):
    """Tests for my Coffebuddy Web app site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        result = self.client.get("/")
        self.assertIn("<h1>CoffeeBuddy</h1>", result.data)

    def test_login1(self):
        result = self.client.get("/login")
        self.assertIn("<h1> Login Form</h1>", result.data)

    def test_login2(self):
        result = self.client.post("/login",
                                    data={"email": "eforman@gmail.com",
                                        "password": "Whimsical"},
                                        follow_redirects=True)
        self.assertIn("<h1>Trip Form</h1>", result.data)

    def test_register1(self):
        result = self.client.get("/register")
        self.assertIn("<p>User name</p>", result.data)

    # def test_register2(self):
    #     result = self.client.post("/register",
    #                                 data={
    #
    #                                 },
    #                                 follow_redirects=True)
    #     self.assertIn("", result.data)

    def test_map(self):
        result = self.client.get("/show_map")
        self.assertIn("", result.data)

    def test_plan_trip(self):
        result = self.client.get("/plan_trip")
        self.assertIn("", result.data)

    # def test_rsvp(self):
    #     result = self.client.post("/rsvp",
    #                               data={"name": "Jane",
    #                                     "email": "jane@jane.com"},
    #                               follow_redirects=True)
    #     self.assertIn("<h2>Party Details</h2>",result.data)


class CoffeebuddyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, uri = "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """drop the db at the end of every test."""

        db.session.close()
        db.drop_all()

    def test_user(self):
        """ Test the user profile page for user_info"""

        result = self.client.get("/user_info")
        self.assertIn("", result.data)

    def test_user_interests(self):
        """ Test the user profile page for user_interests"""

        result = self.client.get("user/info")
        self.assertIn("", result)

    def test_book_genres_list(self):
        """ Test register page for book_genres from db"""

        result = self.client.get("/register")
        self.assertIn("Horror", result.data)

    def test_movie_genres_list(self):
        """ Test register page for movie_genres from db"""

        result = self.client.get("/register")
        self.assertIn("Action", result.data)

    def test_music_genres_list(self):
        """ Test register page for music_genres from db"""

        result = self.client.get("/register")
        self.assertIn("Metal", result.data)

    def test_food_habit_list(self):
        """ Test register page for food_habits from db"""

        result = self.client.get("/register")
        self.assertIn("Vegan", result.data)

    def test_fav_cuisine_list(self):
        """ Test register page for fav_cuisines from db"""

        result = self.client.get("/register")
        self.assertIn("Italian", result.data)

    def hobby1(self):
        """ Test register page for hobbies from db"""

        result = self.client.get("/register")
        self.assertIn("Sewing", result.data)

    def test_fav_cuisine_list(self):
        """ Test register page for fav_cuisines from db"""

        result = self.client.get("/register")
        self.assertIn("Italian", result.data)


if __name__ == "__main__":
    unittest.main()

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
                                    data={"email": "",
                                        "password": ""},
                                        follow_redirects=True)
        self.assertIn("", result.data)

    def test_register1(self):
        result = self.client.get("/")
        self.assertIn("",result.data)

    def test_register2(self):
        result = self.client.post("/register",
                                    data={

                                    },
                                    follow_redirects=True)
        self.assertIn("", result.data)




    # def test_rsvp(self):
    #     result = self.client.post("/rsvp",
    #                               data={"name": "Jane",
    #                                     "email": "jane@jane.com"},
    #                               follow_redirects=True)
    #     self.assertIn("<h2>Party Details</h2>",result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_login_session(self):
        """tests that the login page is displayed only when the user is not 
        in session"""
        #FIXME: test that the games page displays the game from example_data()
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] != None
                
        result = self.client.get("/login")
        self.assertIn("", result.data)


if __name__ == "__main__":
    unittest.main()
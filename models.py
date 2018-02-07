"""Models and database functions for CoffeeBuddy"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions

db = SQLAlchemy()

# Model definitions

class User(db.Model):
    """User of CoffeeBuddy website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    one_word = db.Column(db.String(40), nullable=False)

    interest = db.relationship("Interest",
                            backref=db.backref("User"))


    def __repr__ (self):
        """return personal information about the user"""

        return"< user_id={a}, email={b}, user_name={c}, password={d}, date_of_birth={e}, zipcode={f}, phone={g} >".format(
        a=self.user_id, b=self.email, c=self.user_name, d=self.password, e=self.date_of_birth, f=self.zipcode, 
        g=self.phone)


class Interest(db.Model):
    """User interests and hobbies for matchmaking, Each Column will hold integers 
    that correspond to the information on other tables"""

    __tablename__ = "interests"


    interest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    book_genre_id = db.Column(db.Integer, db.ForeignKey("book_genres.book_genre_id"), nullable=False)
    movie_genre_id = db.Column(db.Integer, db.ForeignKey("movie_genres.movie_genre_id"), nullable=False)
    music_genre_id = db.Column(db.Integer, db.ForeignKey("music_genres.music_genre_id"), nullable=False)
    food_habit_id = db.Column(db.Integer, db.ForeignKey("food_habits.food_habit_id"), nullable=False)
    fav_cuisine_id = db.Column(db.Integer, db.ForeignKey("fav_cuisines.fav_cuisine_id"), nullable=False)
    hobby_id = db.Column(db.Integer,db.ForeignKey("hobbies.hobby_id"), nullable=False)
    political_view_id = db.Column(db.Integer, db.ForeignKey("political_views.political_view_id"), nullable=False)
    religion_id = db.Column(db.Integer,db.ForeignKey("religions.religion_id"), nullable=False)
    outdoor_id = db.Column(db.Integer, db.ForeignKey("outdoors.outdoor_id"), nullable=False)

    def __repr__ (self):
        """return interest choices of the user"""

        d1 ="< interest_id={a}, book_genre_id={b},".format(a=self.interest_id, b=self.book_genre_id)
        d2 =" movie_genre_id={c}, music_genre_id={d},".format(c=self.movie_genre_id, d=self.music_genre_id)
        d3 =" food_habit_id={e}, fav_cuisine_id={f},".format(e=self.food_habit_id, f=self.fav_cuisine_id)
        d4 =" hobby_id={g}, politicial_view_id={h},".format(g=self.hobby_id, h=self.politicial_view_id)
        d5 =" religion_id={i}, outdoor_id={j}>".format(i=self.religion_id, j=self.outdoor_id)

        return d1 + d2 + d3 + d4 + d5


class User_match(db.Model):
    """holds matches made through the history of the app"""

    __tablename__ = "User_matches"

    match_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id_1 = db.Column(db.Integer, nullable=False)
    user_id_2 = db.Column(db.Integer, nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float(Precision=64), nullable=False)
    longitude = db.Column(db.Float(Precision=64), nullable=False)

    def __repr__ (self):
        """return interest choices of the user"""

        return"< match_id={a}, user_id_1={b}, user_id_2={c}, match_date={d}>".format(a=self.match_id, 
        b=self.user_id_1, c=self.user_id_2, d=self.match_date)

class Book_genre(db.Model):
    """Holds the Music_genres and their corresponding ids"""

    __tablename__ = "book_genres"

    book_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_genre_name = db.Column(db.String(40), nullable=False)

    book = db.relationship("Interest",
                            backref=db.backref("Book_genre"))

    def __repr__ (self):
        """displays the ids of Book genres and book genres 
        Can be cross-referenced with the interests table"""

        return"<book_genre_id={}, book_genre_name={}>".format(self.book_genre_id,self.book_genre_name)

class Movie_genre(db.Model):
    """Holds the Movie names and their corresponding ids"""

    __tablename__ = "movie_genres"

    movie_genre_id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_genre_name = db.Column(db.String(40), nullable=False)

    movie = db.relationship("Interest",
                            backref=db.backref("Movie_genre"))

    def __repr__(self):
        """displays the ids of movies and movie names 
        Can be cross-referenced with the interests table"""

        return"<move_genre_id={}, movie_genre_name={}>".format(self.movie_genre_id, self.movie_genre_name)


class Music_genre(db.Model):
    """Holds the Music_genres and their corresponding ids"""

    __tablename__ = "music_genres"

    music_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    music_genre_name = db.Column(db.String(40), nullable=False)

    music = db.relationship("Interest",
                            backref=db.backref("Music_genre"))

    def __repr__ (self):
        """displays the ids of music genres and music genres 
        Can be cross-referenced with the interests table"""

        return"<music_genre_id={}, music_genre_name={}>".format(self.music_genre_id, self.music_genre_name)


class Food_habit(db.Model):
    """Holds the types of food_habits and their corresponding ids """

    __tablename__ = "food_habits"
    
    food_habit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    food_habit_name= db.Column(db.String(40), nullable=False)

    food = db.relationship("Interest",
                            backref=db.backref("Food_Habit"))

    def __repr__ (self):
        """displays the ids of food habits and habit names 
        Can be cross-referenced with the interests table"""

        return"<food_habit_id={}, habit_name={}>".format(self.food_habit_id, self.food_habit_name)


class Fav_cuisine(db.Model):
    """Holds the types of cuisines and thier corresponding ids"""

    __tablename__ = "fav_cuisines"
    
    fav_cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fav_cuisine_name= db.Column(db.String(40), nullable=False)

    cuisine = db.relationship("Interest",
                            backref=db.backref("Fav_cuisine"))

    def __repr__ (self):
        """displays the ids of cuisines and cuisine names 
        Can be cross-referenced with the interests table"""

        return"<fav_cuisine_id={}, fav_cuisine_name={}>".format(self.fav_cuisine_id, self.fav_cuisine_name)


class Hobby(db.Model):
    """Holds the list of hobbies and thier corresponding ids"""

    __tablename__ = "hobbies"
    
    hobby_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hobby_name= db.Column(db.String(40), nullable=False)

    hobby = db.relationship("Interest",
                            backref=db.backref("Hobby"))

    def __repr__ (self):
        """displays the ids of hobbies and hobby names 
        Can be cross-referenced with the interests table"""

        return"<hobby_id={}, hobby_name={}>".format(self.hobby_id, self.hobby_name)


class Political_view(db.Model):
    """Holds the political_views of the users"""

    __tablename__ = "political_views"
    
    political_view_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    political_view_name= db.Column(db.String(40), nullable=False)

    politica_view = db.relationship("Interest",
                            backref=db.backref("Political_view"))

    def __repr__ (self):
        """displays the ids of political views and political view names 
        Can be cross-referenced with the interests table"""

        return"<politicial_view_id={}, political_view_name={}>".format(self.political_view_id, 
        self.political_view_name)


class Religion(db.Model):
    """Holds the religious views and their corresponding ids"""

    __tablename__ = "religions"

    religion_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    religion_name = db.Column(db.String(40), nullable=False)

    religion = db.relationship("Interest",
                            backref=db.backref("Religion"))

    def __repr__ (self):
        """displays the ids of religion and religion names 
        Can be cross-referenced with the interests table"""

        return"<religion_id={}, religion_name={}>".format(self.religion_id, self.religion_name)


class Outdoor(db.Model):
    """Holds the outdoor_activities and their corresponding ids"""

    __tablename__ = "outdoors"

    outdoor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    outdoor_activity = db.Column(db.String(40), nullable=False)

    outdoor = db.relationship("Interest",
                            backref=db.backref("Outdoor"))

    def __repr__ (self):
        """displays the ids of oa, and oa 
        Can be cross-referenced with the interests table"""

        return"<outdoor_id={}, outdoor_activity={}>".format(self.outdoor_id,self.outdoor_activity)
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."

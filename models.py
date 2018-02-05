"""Models and database functions for CoffeeBuddy"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

# Model definitions

class User(db.Model):
    """User of CoffeeBuddy website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.Integer, nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    one_word = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """return personal information about the user"""

        return"< user_id={a}, email={b}, user_name={c}, password={d}, date_of_birth={e}, zipcode={f}, phone={g} >".format(
        a=self.user_id, b=self.email, c=self.user_name, d=self.password, e=self.date_of_birth, f=self.zipcode, 
        g=self.phone)


class Interests(db.Model):
    """User interests and hobbies for matchmaking, Each Column will hold integers 
    that correspond to the information on other tables"""

    __tablename__ = "interests"

    interest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie = db.Column(db.Integer, nullable=False)
    music_genre = db.Column(db.Integer, nullable=False)
    food_habit = db.Column(db.Integer, nullable=False)
    fav_cuisine = db.Column(db.Integer, nullable=False)
    hobby = db.Column(db.Integer, nullable=False)
    political_view = db.Column(db.Integer, nullable=False)
    religion = db.Column(db.Integer, nullable=False)
    fav_spirit = db.Column(db.Integer, nullable=False)
    fav_book = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """return interest choices of the user"""

        return"< user_id={a}, movie={b}, music_genre={c}, food_habit={d}, fav_cuisine={e}, hobby={f}, political_view={g}".format(
        a=self.user_id, b=self.movie, c=self.music_genre, d=self.food_habit, e=self.fav_cuisine, f=self.hobby, 
        g=self.political_view) + "religion={h}, fav_spirit={i}, fav_book={j}>".format(h=self.religion, i=self.fav_spirit, j=self.fav_book)

class User_match(db.Model):
    """holds matches made through the history of the app"""

    __tablename__ = "User_matches"

    match_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id_1 = db.Column(db.Integer, nullable=False)
    user_id_2 = db.Column(db.Integer, nullable=False)
    match_date = db.Column(db.date_time, nullable=False)
    latitude = db.Column(db.Float(Precision=64) nullable=False)
    longitude = db.Column(db.Float(Precision=64) nullable=False)

    def __repr__(self):
        """return interest choices of the user"""

        return"< match_id={a}, user_id_1={b}, user_id_2={c}, match_date={d}>".format(a=self.match_id, 
        b=self.user_id_1, c=self.user_id_2, d=self.match_date)
        

class Movie(db.Model):
    """Holds the Movie names and their corresponding ids"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of movies and movie names 
        Can be cross-referenced with the interests table"""

        return"<move_id={}, movie_name={}>".format(self.movie_id, self.movie_name)


class Music_genre(db.Model):
    """Holds the Music_genres and their corresponding ids"""

    __tablename__ = "music_genres"

    music_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of music genres and music genres 
        Can be cross-referenced with the interests table"""

        return"<music_id={}, genre_name={}>".format(self.music_id, self.genre_name)


class Food_Habit(db.Model):
    """Holds the types of food_habits and their corresponding ids """

    __tablename__ = "food_habits"
    
    food_habit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    habit_name= db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of food habits and habit names 
        Can be cross-referenced with the interests table"""

        return"<food_habit_id={}, habit_name={}>".format(self.food_habit_id, self.habit_name)


class Cuisine(db.Model):
    """Holds the types of cuisines and thier corresponding ids"""

    __tablename__ = "fav_cuisines"
    
    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cuisine_name= db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of cuisines and cuisine names 
        Can be cross-referenced with the interests table"""

        return"<cuisine_id={}, cuisine_name={}>".format(self.cuisine_id, self.cuisine_name)


class Hobby(db.Model):
    """Holds the list of hobbies and thier corresponding ids"""

    __tablename__ = "hobbies"
    
    hobby_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hobby_name= db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of hobbies and hobby names 
        Can be cross-referenced with the interests table"""

        return"<hobby_id={}, hobby_name={}>".format(self.hobby_id, self.hobby_name)


class Political_view(db.Model):
    """Holds the political_views of the users"""

    __tablename__ = "politicial_views"
    
    political_view_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    political_view_name= db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of political views and political view names 
        Can be cross-referenced with the interests table"""

        return"<politicial_view_id={}, political_view_name={}>".format(self.political_view_id, 
        self.political_view_name)


class Religion(db.Model):
    """Holds the religious views and their corresponding ids"""

    __tablename__ = "religions"

    religion_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    religion_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of religion and religion names 
        Can be cross-referenced with the interests table"""

        return"<religion_id={}, religion_name={}>".format(self.religion_id, self.religion_name)



class Spirit(db.Model):
    """Holds the spirits and their corresponding ids"""

    __tablename__ = "spirits"

    spirit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spirit_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of spirit and spirit names
        Can be cross-referenced with the interests table"""

        return"<spirit_id={}, spirit_name={}>".format(self.spirit_id, self.spirit_name)



class Books(db.Model):
    """Holds the Music_genres and their corresponding ids"""

    __tablename__ = "book_genres"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_genre = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of Book genres and book genres 
        Can be cross-referenced with the interests table"""

        return"<book_id={}, book_genre={}>".format(self.book_id,self.book_genre)

class Outdoors(db.Model):
    """Holds the outdoor_activities and their corresponding ids"""

    __tablename__ = "genres"

    outdoor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    outdoor_activity = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """displays the ids of oa, and oa 
        Can be cross-referenced with the interests table"""

        return"<outdoor_id={}, outdoor_activity={}>".format(self.outdoor_id,self.outdoor_activity)
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///coffeebuddy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

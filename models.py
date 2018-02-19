"""Models and database functions for CoffeeBuddy"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

####################################################################################################################

class User(db.Model):
    """User of CoffeeBuddy website."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    one_word = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(250), nullable=True)

    interest = db.relationship('Interest',
                            backref=db.backref('User'))

    def __repr__ (self):
        """return personal information about the user"""

        d1 = '<user_id={a}, email={b},'.format(a=self.user_id, b=self.email)
        d2 = ' user_name={c}, password={d},'.format(c=self.user_name, d=self.password) 
        d3 = ' date_of_birth={e}, zipcode={f},'.format(e=self.date_of_birth, f=self.zipcode)
        d4 = ' phone={g}>'.format(g=self.phone)
        return d1 + d2 + d3 + d4

    
class Interest(db.Model):
    """User interests and hobbies for matchmaking, Each Column will hold integers 
    that correspond to the information on other tables"""

    __tablename__ = 'interests'

    interest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_genre_id = db.Column(db.Integer, db.ForeignKey('book_genres.book_genre_id'), nullable=False)
    movie_genre_id = db.Column(db.Integer, db.ForeignKey('movie_genres.movie_genre_id'), nullable=False)
    music_genre_id = db.Column(db.Integer, db.ForeignKey('music_genres.music_genre_id'), nullable=False)
    food_habit_id = db.Column(db.Integer, db.ForeignKey('food_habits.food_habit_id'), nullable=False)
    fav_cuisine_id = db.Column(db.Integer, db.ForeignKey('fav_cuisines.fav_cuisine_id'), nullable=False)
    hobby_id = db.Column(db.Integer,db.ForeignKey('hobbies.hobby_id'), nullable=False)
    political_view_id = db.Column(db.Integer, db.ForeignKey("political_views.political_view_id"), nullable=False)
    religion_id = db.Column(db.Integer,db.ForeignKey('religions.religion_id'), nullable=False)
    outdoor_id = db.Column(db.Integer, db.ForeignKey('outdoors.outdoor_id'), nullable=False)

    def __repr__ (self):
        """return interest choices of the user"""

        d1 ='< interest_id={a}, book_genre_id={b},'.format(a=self.interest_id, b=self.book_genre_id)
        d2 =' movie_genre_id={c}, music_genre_id={d},'.format(c=self.movie_genre_id, d=self.music_genre_id)
        d3 =' food_habit_id={e}, fav_cuisine_id={f},'.format(e=self.food_habit_id, f=self.fav_cuisine_id)
        d4 =' hobby_id={g}, politicial_view_id={h},'.format(g=self.hobby_id, h=self.political_view_id)
        d5 =' religion_id={i}, outdoor_id={j}>'.format(i=self.religion_id, j=self.outdoor_id)

        return d1 + d2 + d3 + d4 + d5


class UserMatch(db.Model):
    """holds matches made through the history of the app"""

    __tablename__ = "user_matches"

    match_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id_1 = db.Column(db.Integer, nullable=False)
    user_id_2 = db.Column(db.Integer, nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float(Precision=64), nullable=False)
    longitude = db.Column(db.Float(Precision=64), nullable=False)

    def __repr__ (self):
        """return interest choices of the user"""

        return'< match_id={a}, user_id_1={b}, user_id_2={c}, match_date={d}>'.format(a=self.match_id, 
        b=self.user_id_1, c=self.user_id_2, d=self.match_date)

class PendingMatch(db.Model):
    """holds a list of all pending matches for user queries"""

    __tablename__ = "pending_matches"

    user_query_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    query_pin_code = db.Column(db.Integer, nullable=False)
    query_time = db.Column(db.DateTime, nullable=False)
    pending = db.Column(db.Boolean, nullable=False)

    def __repr__ (self):
        """return information about a user query"""

        d1 = "<user_query_id={a}, user_id={b},".format(a=self.user_query_id,b=self.user_id)
        d2 = " query_pin_code={c}, query_time={d},".format(c=self.query_pin_code,d=self.query_time)
        d3 = " pending={e}>".format(e=self.pending)

        return d1 + d2 + d3

class BookGenre(db.Model):
    """Holds the Music_genres and their corresponding ids"""

    __tablename__ = 'book_genres'

    book_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_genre_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('book_genre'))

    def __repr__ (self):
        """displays the ids of Book genres and book genres 
        Can be cross-referenced with the interests table"""

        return'<book_genre_id={}, book_genre_name={}>'.format(self.book_genre_id,self.book_genre_name)


class MovieGenre(db.Model):
    """Holds the Movie names and their corresponding ids"""

    __tablename__ = 'movie_genres'

    movie_genre_id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_genre_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('movie_genre'))

    def __repr__(self):
        """displays the ids of movies and movie names 
        Can be cross-referenced with the interests table"""

        return'<move_genre_id={}, movie_genre_name={}>'.format(self.movie_genre_id, self.movie_genre_name)


class MusicGenre(db.Model):
    """Holds the Music_genres and their corresponding ids"""

    __tablename__ = 'music_genres'

    music_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    music_genre_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('music_genre'))

    def __repr__ (self):
        """displays the ids of music genres and music genres 
        Can be cross-referenced with the interests table"""

        return'<music_genre_id={}, music_genre_name={}>'.format(self.music_genre_id, self.music_genre_name)


class FoodHabit(db.Model):
    """Holds the types of food_habits and their corresponding ids """

    __tablename__ = 'food_habits'
    
    food_habit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    food_habit_name= db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('food_habit'))

    def __repr__ (self):
        """displays the ids of food habits and habit names 
        Can be cross-referenced with the interests table"""

        return'<food_habit_id={}, habit_name={}>'.format(self.food_habit_id, self.food_habit_name)


class FavCuisine(db.Model):
    """Holds the types of cuisines and thier corresponding ids"""

    __tablename__ = 'fav_cuisines'
    
    fav_cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fav_cuisine_name= db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('fav_cuisine'))

    def __repr__ (self):
        """displays the ids of cuisines and cuisine names 
        Can be cross-referenced with the interests table"""

        return'<fav_cuisine_id={}, fav_cuisine_name={}>'.format(self.fav_cuisine_id, self.fav_cuisine_name)


class Hobby(db.Model):
    """Holds the list of hobbies and thier corresponding ids"""

    __tablename__ = 'hobbies'
    
    hobby_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hobby_name= db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('hobby'))

    def __repr__ (self):
        """displays the ids of hobbies and hobby names 
        Can be cross-referenced with the interests table"""

        return'<hobby_id={}, hobby_name={}>'.format(self.hobby_id, self.hobby_name)


class PoliticalView(db.Model):
    """Holds the political_views of the users"""

    __tablename__ = 'political_views'
    
    political_view_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    political_view_name= db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('political_view'))

    def __repr__ (self):
        """displays the ids of political views and political view names 
        Can be cross-referenced with the interests table"""

        return'<politicial_view_id={}, political_view_name={}>'.format(self.political_view_id, 
        self.political_view_name)


class Religion(db.Model):
    """Holds the religious views and their corresponding ids"""

    __tablename__ = 'religions'

    religion_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    religion_name = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('religion'))

    def __repr__ (self):
        """displays the ids of religion and religion names 
        Can be cross-referenced with the interests table"""

        return'<religion_id={}, religion_name={}>'.format(self.religion_id, self.religion_name)


class Outdoor(db.Model):
    """Holds the outdoor_activities and their corresponding ids"""

    __tablename__ = 'outdoors'

    outdoor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    outdoor_activity = db.Column(db.String(40), nullable=False)

    interest = db.relationship('Interest',
                            backref=db.backref('outdoor'))

    def __repr__ (self):
        """displays the ids of oa, and oa 
        Can be cross-referenced with the interests table"""

        return'<outdoor_id={}, outdoor_activity={}>'.format(self.outdoor_id,self.outdoor_activity)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""

    user1 = User(fname="Felix", lname="Alvarez", email="fez@hotmail.com",
                user_name="FezAl", password="Friend", date_of_birth="2-20-1989",
                zipcode="95134", phone="657897149", one_word="hello")
    user2 = User(fname="Donna", lname="Pinciotti", email="donnap@hotmail.com",
                user_name="donpin", password="seventies", date_of_birth="7-18-1989",
                zipcode="95111", phone="5098799711", one_word="honey")
    user3 = User(fname="Eric", lname="Forman", email="eforman@gmail.com",
                user_name="Efor", password="Whimsical", date_of_birth="4-16-1989",
                zipcode="95122", phone="6509908999", one_word="healthy")
    user4 = User(fname="Kelso", lname="Harry", email="kels@hotmail.com",
                user_name="kel", password="Dudes", date_of_birth="9-9-1989",
                zipcode="95114", phone="789891849", one_word="pretty")
    user_interest1 = Interest(user_id=1, book_genre_id=2, movie_genre_id=1, 
                            music_genre_id=1, food_habit_id=2,fav_cuisine_id=2,
                            hobby_id=2, political_view_id=1, religion_id=1,
                            outdoor_id=1)
    user_interest2 = Interest(user_id=2, book_genre_id=1, movie_genre_id=1, 
                            music_genre_id=1, food_habit_id=1,fav_cuisine_id=2,
                            hobby_id=2, political_view_id=2, religion_id=2,
                            outdoor_id=1)
    user_interest3 = Interest(user_id=3, book_genre_id=2, movie_genre_id=1, 
                            music_genre_id=1, food_habit_id=2,fav_cuisine_id=2,
                            hobby_id=1, political_view_id=1, religion_id=1,
                            outdoor_id=2)
    user_interest4 = Interest(user_id=4, book_genre_id=1, movie_genre_id=1, 
                            music_genre_id=1, food_habit_id=1,fav_cuisine_id=2,
                            hobby_id=2, political_view_id=1, religion_id=2,
                            outdoor_id=1)
    pending_match1 = PendingMatch(user_id=3, query_pin_code=95111, query_time='2018-02-15 22:20:21.313644', pending=True)
    pending_match2 = PendingMatch(user_id=4, query_pin_code=95111, query_time='2018-02-15 22:20:21.313644', pending=True)
    book_genre1 = BookGenre(book_genre_name="Horror")
    book_genre2 = BookGenre(book_genre_name="Fiction")
    movie_genre1 = MovieGenre(movie_genre_name="Action")
    movie_genre2 = MovieGenre(movie_genre_name="Comedy")
    music_genre1 = MusicGenre(music_genre_name="Metal")
    music_genre2 = MusicGenre(music_genre_name="Jazz")
    food_habit1 = FoodHabit(food_habit_name="Vegan")
    food_habit2 = FoodHabit(food_habit_name="Pescetarian")
    fav_cuisine1 = FavCuisine(fav_cuisine_name="Italian")
    fav_cuisine2 = FavCuisine(fav_cuisine_name="Mexican")
    hobby1 = Hobby(hobby_name="Sewing")
    hobby2 = Hobby(hobby_name="Knitting")
    political_view1 = PoliticalView(political_view_name="Democrat")
    political_view2 = PoliticalView(political_view_name="Republic")
    religion1 = Religion(religion_name="Hindu")
    religion2 = Religion(religion_name="Christian")
    outdoor1 = Outdoor(outdoor_activity="hiking")
    outdoor2 = Outdoor(outdoor_activity="swimming")

    db.session.add_all([user1, user2, user3, user4,
                        user_interest1, user_interest2, user_interest3, user_interest4,
                        pending_match1, pending_match2,
                        book_genre1, book_genre2, movie_genre1, movie_genre2,
                        music_genre1, music_genre2, food_habit1, food_habit2,
                        fav_cuisine1, fav_cuisine2, hobby1, hobby2,
                        political_view1, political_view2,religion1, religion2,
                        outdoor1, outdoor_id])

    db.session.commit()
    

###################################################################################################################

if __name__ == "__main__":
    
    from server import app
    connect_to_db(app)
    db.create_all()
    print 'Connected to DB.'

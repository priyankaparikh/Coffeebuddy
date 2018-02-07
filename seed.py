"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from models import connect_to_db, db
from server import app
from models import User
from models import Book_genre
from models import Movie_genre
from models import Music_genre
from models import Food_habit
from models import Fav_cuisine
from models import Hobby
from models import Political_view
# from models import Food_habit
# from models import Fav_cuisine
from faker import Faker

def load_users():
    """Load users from static/user_data.txt into database."""

    print "User"
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/user_data.txt"):
        row = row.rstrip()
        #is this pythonic ?
        user_id, fname, lname, email, user_name, password, date_of_birth, zipcode, phone, one_word = row.split("|")

        user = User(user_id=user_id,
                    fname=fname,
                    lname=lname,
                    email=email,
                    user_name=user_name,
                    password=password,
                    date_of_birth=date_of_birth,
                    zipcode=zipcode,
                    phone=phone,
                    one_word=one_word)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_books():
    """Load books from book_genre_data into database."""

    print "Book_genre"
    User.query.delete()

    for row in open("seed_data/book_genre_data.txt"):
        row = row.rstrip()
        book_genre_id, book_genre_name = row.split("|")

        book = Book_genre(book_genre_id=book_genre_id,
                          book_genre_name=book_genre_name)

        db.session.add(book)

    db.session.commit()


def load_movies():
    """Load movies from movie_genre_data into database."""

    print "Movie_genre"
    User.query.delete()

    for row in open("seed_data/movie_genre_data.txt"):
        row = row.rstrip()
        movie_genre_id, movie_genre_name = row.split("|")

        movie = Movie_genre(movie_genre_id=movie_genre_id,
                          movie_genre_name=movie_genre_name)

        db.session.add(movie)

    db.session.commit()


def load_music():
    """Load music from music_genre_data into database."""

    print "music_genre"
    User.query.delete()

    for row in open("seed_data/music_genre_data.txt"):
        row = row.rstrip()
        music_genre_id, music_genre_name = row.split("|")

        music = Music_genre(music_genre_id=music_genre_id,
                          music_genre_name=music_genre_name)

        db.session.add(music)

    db.session.commit()


def load_food_habits():
    """Load food_habits from food_habit_data into database."""

    print "Food_habit"
    User.query.delete()

    for row in open("seed_data/food_habit_data.txt"):
        row = row.rstrip()
        food_habit_id, food_habit_name = row.split("|")

        habit = Food_habit(food_habit_id=food_habit_id,
                          food_habit_name=food_habit_name)

        db.session.add(habit)

    db.session.commit()


def load_cuisines():
    """Load  from fav_cuisine_data into database."""

    print "Fav_cuisine"
    User.query.delete()

    for row in open("seed_data/fav_cuisine_data.txt"):
        row = row.rstrip()
        fav_cuisine_id, fav_cuisine_name = row.split("|")

        cuisine = Fav_cuisine(fav_cuisine_id=fav_cuisine_id,
                          fav_cuisine_name=fav_cuisine_name)

        db.session.add(cuisine)

    db.session.commit()


def load_hobbies():
    """Load  from hobby_data_data into database."""

    print "Hobby"
    User.query.delete()

    for row in open("seed_data/hobby_data.txt"):
        row = row.rstrip()
        hobby_id, hobby_name = row.split("|")

        hobby = Hobby(hobby_id=hobby_id,
                          hobby_name=hobby_name)

        db.session.add(hobby)

    db.session.commit()


def load_political_views():
    """Load  from book_genre_data into database."""

    print "Political_views"
    User.query.delete()

    for row in open("seed_data/political_view_data.txt"):
        row = row.rstrip()
        political_view_id, political_view_name = row.split("|")

        view = Political_view(political_view_id=political_view_id,
                              political_view_name=political_view_name)

        db.session.add(view)

    db.session.commit()


def load_religions():
    """Load  from book_genre_data into database."""

    print "Religions"
    User.query.delete()

    for row in open("seed_data/religion_data.txt"):
        row = row.rstrip()
        religion_id, religion_name = row.split("|")

        religion = Religion(religion_id=religion_id,
                            religion_name=religion_name)

        db.session.add(religion)

    db.session.commit()


def outdoor_activities():
    """Load  from book_genre_data into database."""

    print "Outdoors"
    User.query.delete()

    for row in open("seed_data/outdoor_data.txt"):
        row = row.rstrip()
        outdoor_id, outdoor_activity = row.split("|")

        outdoor = Political_view(outdoor_id=outdoor_id,
                              outdoor_activity=outdoor_activity)

        db.session.add(outdoor)

    db.session.commit()
# def load_ratings():
#     """Load ratings from u.data into database."""


# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_books()
    load_movies()
    load_music()
    load_food_habits()
    load_cuisines()
    load_hobbies()
    load_political_views()
    load_religions()

    # set_val_user_id()

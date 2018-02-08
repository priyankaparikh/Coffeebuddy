"""Utility file to seed the coffeebuddy database from generated data in seed_data"""
from sqlalchemy import func
from models import connect_to_db, db
from models import *
from random import choice
#import pdb; pdb.set_trace()

def load_users():
    """Load users from static/user_data.txt into database."""

    print "User"
    User.query.delete()

    file = open("seed_data/user_data.txt")
    for row in file:
        row = row.rstrip()
        row = row.split("|")
        
        user_id = row[0]
        fname = row[1]
        lname = row[2]
        email = row[3]
        user_name = row[4]
        password = row[5]
        date_of_birth = row[6]
        zipcode = row[7]
        phone = row[8]
        one_word = row[9]

        #insert user
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

        db.session.add(user)

    db.session.commit()


def load_books():
    """Load books from book_genre_data into database."""

    print "BookGenre"

    #read book_genre_data
    for row in open("seed_data/book_genre_data.txt"):
        row = row.rstrip()
        book_genre_id, book_genre_name = row.split("|")
        # insert book genre
        book = BookGenre(book_genre_id=book_genre_id,
                          book_genre_name=book_genre_name)

        db.session.add(book)

    db.session.commit()


def load_movies():
    """Load movies from movie_genre_data into database."""

    print "MovieGenre"

    for row in open("seed_data/movie_genre_data.txt"):
        row = row.rstrip()
        movie_genre_id, movie_genre_name = row.split("|")
        #insert movie
        movie = MovieGenre(movie_genre_id=movie_genre_id,
                          movie_genre_name=movie_genre_name)

        db.session.add(movie)

    db.session.commit()


def load_music():
    """Load music from music_genre_data into database."""

    print "MusicGenre"

    for row in open("seed_data/music_genre_data.txt"):
        row = row.rstrip()
        music_genre_id, music_genre_name = row.split("|")
        #insert music
        music = MusicGenre(music_genre_id=music_genre_id,
                          music_genre_name=music_genre_name)

        db.session.add(music)

    db.session.commit()


def load_food_habits():
    """Load food_habits from food_habit_data into database."""

    print "FoodHabit"

    for row in open("seed_data/food_habit_data.txt"):
        row = row.rstrip()
        food_habit_id, food_habit_name = row.split("|")
        #insert habit
        habit = FoodHabit(food_habit_id=food_habit_id,
                          food_habit_name=food_habit_name)

        db.session.add(habit)

    db.session.commit()


def load_cuisines():
    """Load  from fav_cuisine_data into database."""

    print "FavCuisine"
  
    for row in open("seed_data/fav_cuisine_data.txt"):
        row = row.rstrip()
        fav_cuisine_id, fav_cuisine_name = row.split("|")
        #insert cuisine
        cuisine = FavCuisine(fav_cuisine_id=fav_cuisine_id,
                          fav_cuisine_name=fav_cuisine_name)

        db.session.add(cuisine)

    db.session.commit()


def load_hobbies():
    """Load  from hobby_data_data into database."""

    print "Hobby"

    for row in open("seed_data/hobby_data.txt"):
        row = row.rstrip()
        hobby_id, hobby_name = row.split("|")
        #insert hobby
        hobby = Hobby(hobby_id=hobby_id,
                          hobby_name=hobby_name)

        db.session.add(hobby)

    db.session.commit()


def load_political_views():
    """Load  from book_genre_data into database."""

    print "PoliticalViews"


    for row in open("seed_data/political_view_data.txt"):
        row = row.rstrip()
        political_view_id, political_view_name = row.split("|")
        #insert political view
        view = PoliticalView(political_view_id=political_view_id,
                              political_view_name=political_view_name)

        db.session.add(view)

    db.session.commit()


def load_religions():
    """Load  from book_genre_data into database."""

    print "Religions"

    for row in open("seed_data/religion_data.txt"):
        row = row.rstrip()
        religion_id, religion_name = row.split("|")
        #insert religion
        religion = Religion(religion_id=religion_id,
                            religion_name=religion_name)

        db.session.add(religion)

    db.session.commit()



def load_outdoor_activities():
    """Load  from book_genre_data into database."""

    print "Outdoors"

    for row in open("seed_data/outdoor_data.txt"):
        row = row.rstrip()
        outdoor_id, outdoor_activity = row.split("|")
        #insert outdoor
        outdoor = Outdoor(outdoor_id=outdoor_id,
                              outdoor_activity=outdoor_activity)

        db.session.add(outdoor)

    db.session.commit()


def seed_interests():
    """ add data for each user in the interest table"""

    books = BookGenre.query.all()
    movies = MovieGenre.query.all()
    music = MusicGenre.query.all() 
    food_habits = FoodHabit.query.all()
    cuisines = FavCuisine.query.all()
    hobbies = Hobby.query.all()
    political_views = PoliticalView.query.all()
    religions = Religion.query.all()
    outdoors = Outdoor.query.all()
    users = User.query.all()

    for user in users:
        new_interest_row = Interest(user_id=user.user_id,
                                    book_genre_id=choice(books).book_genre_id,
                                    movie_genre_id=choice(movies).movie_genre_id,
                                    music_genre_id=choice(music).music_genre_id,
                                    food_habit_id=choice(food_habits).food_habit_id,
                                    fav_cuisine_id=choice(cuisines).fav_cuisine_id,
                                    hobby_id=choice(hobbies).hobby_id,
                                    political_view_id=choice(political_views).political_view_id,
                                    religion_id=choice(religions).religion_id,
                                    outdoor_id=choice(outdoors).outdoor_id
                                    )

        db.session.add(new_interest_row)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


########################################################################################################

if __name__ == "__main__":
    from flask import Flask 
    from server import app
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
    load_outdoor_activities()
    seed_interests()
    set_val_user_id()

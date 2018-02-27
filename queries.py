"""test the models for database querys"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import *
from functools import wraps
from flask import Flask, render_template, redirect, request, flash, session, g

#################################################################################################

def login_req(f):
    """ This function is
    - is a view decorator that wraps routes where the user
    has to be logged in to view the contents
    - if the user is not logged in it redirects the user to
    the Homepage
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please log in or register.")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def get_user_id(input_email):
    """return the only user_id of a user

    >>> get_user_id('LeahChavez@gmail.com')
    489
    """

    user = User.query.filter(User.email == '{}'.format(input_email)).all()

    # at this point our user looks something like this :
    #[<user_id=489, email=LeahChavez@gmail.com, user_name=LhCv,
    # password=bZ@KRW@k+4, #date_of_birth=1983-04-29,
    #zipcode=24568, phone=+96(5)2036281580>]

    user_id = user[0].user_id

    return user_id


def get_user_name(input_id):
    """accepts a user_id as a parameter and returns a tuple of the fname
    and lname of the user"""

    user = User.query.filter(User.user_id == '{}'.format(input_id)).first()

    return ('{}'.format(user.fname), '{}'.format(user.lname))


def get_user_info(input_id):
    """return user_info as a list using the user_id

    >>> get_user_info('280')
    [280, u'EricaBrown@fastmail.com', u'EcBw', u'1990-01-13', u'27359', u'+47(7)9589562562']

    """

    user = User.query.filter(User.user_id == input_id).all()

    user_id = user[0].user_id
    email = user[0].email
    user_name = user[0].user_name
    date_of_birth = user[0].date_of_birth
    zipcode = user[0].zipcode
    phone = user[0].phone
    fname = user[0].fname
    lname = user[0].lname
    profile_picture = user[0].profile_picture


    return [user_id, email, user_name,
            date_of_birth, zipcode, phone,
            fname, lname, profile_picture]


def validate_password(input_email, input_password):
    """check if an email and password are valid

    >>> validate_password('CarolMason@aol.com ','6LUZzfiN(Z')
    True

    >>> validate_password('CynthiaGibson@gmail.com','T^^+5BQvS3')
    True

    """

    user = User.query.filter(User.email == '{}'.format(input_email)).first()
    password = user.password
    email = user.email

    return password == input_password and email == input_email


def all_book_genres():
    """returns a list of tuples with book genre ids and book genres
    """

    book_genres = BookGenre.query.all()
    books = []

    for book in book_genres:
        books.append((book.book_genre_id, book.book_genre_name))

    return ["Preferred book genre", books]


def all_movie_genres():
    """returns a list of tuples with book genre ids and book genres"""

    movie_genres = MovieGenre.query.all()
    movies = []

    for movie in movie_genres:
        movies.append((movie.movie_genre_id, movie.movie_genre_name))

    return ["Preferred movie genre", movies]


def all_music_genres():
    """returns a list of tuples with book genre ids and book genres"""

    music_genres = MusicGenre.query.all()
    music = []

    for music_genre in music_genres:
        music.append((music_genre.music_genre_id,
                         music_genre.music_genre_name))

    return ["Preferred music genre", music]


def all_food_habits():
    """ returns a list of tuples with food habit ids and habit names"""

    food_habits = FoodHabit.query.all()
    food = []

    for habit in food_habits:
        food.append((habit.food_habit_id, habit.food_habit_name))

    return ["Food habits", food]


def all_fav_cuisines():
    """ returns a list of tuples with favorite cuisine ids and habit names"""

    fav_cuisines = FavCuisine.query.all()
    cuisines = []

    for cuisine in fav_cuisines:
        cuisines.append((cuisine.fav_cuisine_id, cuisine.fav_cuisine_name))

    return ["Preferred cuisine type", cuisines]


def all_hobbies():
    """ returns a list of tuples with hobby ids and hobby names"""
    hobbies = Hobby.query.all()
    hobby = []

    for curr_hobby in hobbies:
        hobby.append((curr_hobby.hobby_id, curr_hobby.hobby_name))

    return ["Favorite hobby", hobby]


def all_political_views():
    """
        returns a list of tuples with political views ids
        and political views names
    """
    political_views = PoliticalView.query.all()
    political_view = []

    for curr_pol_view in political_views:
        political_view.append((curr_pol_view.political_view_id,
                               curr_pol_view.political_view_name))

    return ["Political ideology", political_view]


def all_religions():
    """
        returns a list of tuples with religion ids
        and religion names
    """
    religions = Religion.query.all()
    rel = []

    for religion in religions:
        rel.append((religion.religion_id,
                               religion.religion_name))

    return ["Religious ideology", rel]


def all_outdoors():
    """
        returns a list of tuples with outdoor_activity ids
        and outdoor activity names
    """
    all_outdoors = Outdoor.query.all()
    activities = []

    for out in all_outdoors:
        activities.append((out.outdoor_id,
                               out.outdoor_activity))

    return ["Favorite Outdoor activity", activities]


def query_pending_match(pincode):
    """a list of user_id that need to be matched"""

    potential_matches = []

    users = PendingMatch.query.filter(PendingMatch.pending == True,
                                    PendingMatch.query_pin_code == pincode).all()

    for i in users:
        user_id = i.user_id
        potential_matches.append(user_id)

    return potential_matches


def get_user_interests(user_id):
    """returns a user object for futher analysis
    get_user_info(251)
    [251, u'JamesFuentes@fastmail.com', u'JeFns', u'1998-02-16',
    u'08707', u'(074)590-8409x0046', u'James', u'Fuentes',
    u'/static/user_profile_pictures/pexels-photo-354951.jpeg']
    """

    user = Interest.query.filter(Interest.user_id == user_id).first()

    return user


def update_user_info(info):
    """dynamically updates user_information by checking the data type of the input"""

    pass



#######################################################################################
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    db.create_all()
    import doctest

    result = doctest.testmod()
    if not result.failed:
        print("All tests passed!")

    print "Connected to DB."

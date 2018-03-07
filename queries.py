""" Utility file that queries the Database. """

from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import *
from functools import wraps
from flask import Flask, render_template, redirect, request, flash, session, g
import datetime

#################################################################################################

def login_req(f):
    """ A view decorator that wraps routes where the user
        has to be logged in to view the contents. If the user is not
        logged in it redirects the user to the Homepage.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please log in or register.")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def plan_trip_req(f):
    """ A view decorator that wraps routes where the user
        has to have a planned trip to view the profiles of other users.
        If the user does not have a trip planned it redirects to the
        plan_trip page.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("'query_time'") is None:
            flash("Please plan a trip.")
            return redirect("/plan_trip")
        return f(*args, **kwargs)
    return decorated_function


def get_user_id(input_email):
    """ Queries the users table and accepts an email as input
        INPUT FORMAT = string
        Returns the the only user_id of a user
        OUTPUT FORMAT = integer
    """

    user = User.query.filter(User.email == '{}'.format(input_email)).all()
    user_id = user[0].user_id
    return user_id


def get_user_name(input_id):
    """ Accepts a user_id as a parameter and returns a tuple of the fname
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


def get_all_made_matches(user_id):
    """ Accepts a user_id as a parameter and returns a list of
    user names and images that the user made succesful matches with
    - Calls the get_user_info function which returns :
        [2, u'PatriciaTorres@hotmail.com', u'PriTr',
        u'1999-01-15', u'25076', u'00543301160',
        u'Patricia', u'Torres',
        u'/static/user_profile_pictures/pexels-photo-634030.jpeg']
    - Returns a list of tuples with the user_name as the first element
     and profile picture as the second element
    """
    # query the user_matches table
    check_matches = UserMatch.query.filter(UserMatch.user_id_1 == user_id,
                                         UserMatch.user_2_status == True)

    matches = check_matches.all()
    all_match_info = []

    for match in matches:
        user_id2 = match.user_id_2
        user_info = get_user_info(user_id2)
        user_name = user_info[6] + " " + user_info[7]
        all_match_info.append(user_name, user_info[-1])

    return all_match_info

def get_user_phone(user_id):
    """ Gets the userphone number """

def validate_password(input_email, input_password):
    """ This function
    - Checks if an email and password are valid by:
    - Querying the db for the input email id
    - Querying for the password of the same user

    >>> validate_password('CarolMason@aol.com ','6LUZzfiN(Z')
    True

    >>> validate_password('CynthiaGibson@gmail.com','T^^+5BQvS3')
    True

    """

    user = User.query.filter(User.email == '{}'.format(input_email)).first()
    password = user.password
    email = user.email

    return password == input_password and email == input_email


def get_max_id(input_table_id):
    """ This function checks the table for the max value of the input
    table id
    """
    max_id = db.session.query(func.max(input_table_id)).one()
    return int(max_id[0])


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


def get_user_interests(user_id):
    """ This function
    - Queries the user_interests table
    - Returns an interest object with all the interest ids
    """
    user = Interest.query.filter(Interest.user_id == user_id).first()

    return user

def get_interest_name(interest_id, table_name):
    """ This function
    - Queries the table for an a specific id
    - Returns the value
    """

    Interest = table_name.query.filter(Interest.user_id == user_id).first()


def get_interest_info(interest_info):
    """  Accepts a SINGLE tuple format: (int, int)
        - The first element of the tuple is the value of the interest
        - The second element is the table id
        - Assigns the queries to a small dictionary in this order:
        - user.interest_id          |(0)
        - user.book_genre_id        |(1)
        - user.movie_genre_id       |(2)
        - user.music_genre_id       |(3)
        - user.food_habit_id        |(4)
        - user.fav_cuisine_id       |(5)
        - user.hobby_id             |(6)
        - user.political_view_id    |(7)
        - user.religion_id          |(8)
        - user.outdoor_id           |(9)
    """

    common_value = interest_info[0]
    table_id = interest_info[1]

    id_info = { 1 : BookGenre.query.filter(BookGenre.book_genre_id == common_value),
                2 : MovieGenre.query.filter(MovieGenre.movie_genre_id == common_value),
                3 : MusicGenre.query.filter(MusicGenre.music_genre_id == common_value),
                4 : FoodHabit.query.filter(FoodHabit.food_habit_id == common_value),
                5 : FavCuisine.query.filter(FavCuisine.fav_cuisine_id == common_value),
                6 : Hobby.query.filter(Hobby.hobby_id == common_value),
                7 : PoliticalView.query.filter(PoliticalView.political_view_id == common_value),
                8 : Religion.query.filter(Religion.religion_id == common_value),
                9 : Outdoor.query.filter(Outdoor.outdoor_id == common_value) }

    interest_details = id_info[table_id].first()

    return interest_details

def get_user_match(user_id):
    """ This function
        - Checks the db for a specific user if the user is a potential match already
        - Returns a
    """

    q1 = UserMatch.query
    fil = q1.filter(UserMatch.user_id_2 == 339, UserMatch.user_2_status == False).all()


def update_matched(user_id1, user_id2, query_time):
    """ Accepts 2 user ids as an input.
        - user_id1 is the logged in user.
        - user_id2 is the user choice.
        - query time of the users
        Checks UserMatch table for a pending match.
        Returns True if a match is made
    """

    time = datetime.datetime.now()
    match = UserMatch.query.filter(UserMatch.user_id_2 == user_id1,
                                    UserMatch.user_id_1 == user_id2,
                                    UserMatch.user_2_status == False)

    # check pending_matches table for both user user_ids
    # if both have clicked on each other update the db to change
    # the user status to false
    pending_match = match.first()

    if pending_match:
        pending_match.user_2_status = True
        db.session.commit()
        return True

    return False


def find_valid_matches(user_id_1, pincode, query_time):
    """ Accepts user_id, pincode, query_time as inputs
    user_id = integer
    pincode = integer
    query_time = string
    eg => validate_trip(399, 95134,"2018-02-28 20:30:00")
    - queries the pending_match for an already updated query
    - returns if a trip query of a user is valid
    - The query time is a string for now
    """
    potential_matches = []
    # creates an object from the input date string

    # finding matches for the same query time
    query_time_obj = datetime.datetime.strptime(query_time, "%Y-%m-%d %H:%M:%S")

    # check for all pending_matches
    trip_q = PendingMatch.query.filter(PendingMatch.query_pin_code == pincode,
                                        func.date(PendingMatch.query_time) == query_time_obj.date(),
                                        PendingMatch.pending == True)

    users = trip_q.all()

    for i in users:
        user_id = i.user_id
        potential_matches.append(user_id)

    return potential_matches

def find_trip_count(user_id):
    """ Queries the PendingMatch table for a specific user's trip requests
        Queries the UserMatch table for a user's matches
    """

    all_pm = PendingMatch.query.filter(PendingMatch.user_id == user_id).all()
    all_sm = UserMatch.query.filter(UserMatch.user_id_1 == user_id).all()

    return [len(all_pm), len(all_sm)]




def clean_time(str_tme):
    """ Helper function to clean a string that comes from the html date input """

    chars = str_tme.split('T')
    tm = (" ").join(chars)
    return tm + ":00"


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

""" Utility file that queries the Database. """

from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import *
from functools import wraps
from flask import Flask, render_template, redirect, request, flash, session, g
import datetime

##################################################################################

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
    """ Queries the users table and accepts an email as input.
        INPUT FORMAT = String.
        Returns the the only user_id of a user.
        OUTPUT FORMAT = Integer.
    """

    user = User.query.filter(User.email == '{}'.format(input_email)).all()
    user_id = user[0].user_id
    return user_id


def get_user_name(input_id):
    """ Queries the users table and accepts a userid as input.
        INPUT FORMAT = digit.
        Returns the fname and lname of the said user.
        OUTPUT FORMAT = list of strings.
    """

    user = User.query.filter(User.user_id == '{}'.format(input_id)).first()

    return ('{}'.format(user.fname), '{}'.format(user.lname))


def get_user_info(input_id):
    """ Queries the users table and accepts a userid as input.
        INPUT FORMAT = Integer.
        Returns user_info as a list using the user_id.
        OUTPUT FORMAT = string.
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
    """ Queries the user_matches table and accepts a userid as input.
        INPUT FORMAT = Integer.
        Returns a list of tuples with the first element as the user name
        and the second element as the url to the profile picture.
        OUTPUT FORMAT = list of tuples of strings.
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


def validate_password(input_email, input_password):
    """ Queries the users table and accepts email and password as inputs.
        INPUT FORMAT = string, string.
        Returns a Boolean.
        OUTPUT FORMAT = Boolean.
    """

    user = User.query.filter(User.email == '{}'.format(input_email)).first()
    password = user.password
    email = user.email

    return password == input_password and email == input_email


def get_max_id(input_table_id):
    """ Queries a given table.
        INPUT FORMAT = Integer.
        Returns a max count for the primary key of the given table.
        OUTPUT FORMAT = Integer.
    """

    max_id = db.session.query(func.max(input_table_id)).one()
    return int(max_id[0])


def all_book_genres():
    """ Queries the book_genres table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    book_genres = BookGenre.query.all()
    books = []

    for book in book_genres:
        books.append((book.book_genre_id, book.book_genre_name))

    return ["Preferred book genre", books]


def all_movie_genres():
    """ Queries the movie_genres table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    movie_genres = MovieGenre.query.all()
    movies = []

    for movie in movie_genres:
        movies.append((movie.movie_genre_id, movie.movie_genre_name))

    return ["Preferred movie genre", movies]


def all_music_genres():
    """ Queries the music_genres table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    music_genres = MusicGenre.query.all()
    music = []

    for music_genre in music_genres:
        music.append((music_genre.music_genre_id,
                         music_genre.music_genre_name))

    return ["Preferred music genre", music]


def all_food_habits():
    """ Queries the food_habits table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    food_habits = FoodHabit.query.all()
    food = []

    for habit in food_habits:
        food.append((habit.food_habit_id, habit.food_habit_name))

    return ["Food habits", food]


def all_fav_cuisines():
    """ Queries the fav_cuisines table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    fav_cuisines = FavCuisine.query.all()
    cuisines = []

    for cuisine in fav_cuisines:
        cuisines.append((cuisine.fav_cuisine_id, cuisine.fav_cuisine_name))

    return ["Preferred cuisine type", cuisines]


def all_hobbies():
    """ Queries the hobbies table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    hobbies = Hobby.query.all()
    hobby = []

    for curr_hobby in hobbies:
        hobby.append((curr_hobby.hobby_id, curr_hobby.hobby_name))

    return ["Favorite hobby", hobby]


def all_political_views():
    """ Queries the political_views table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    political_views = PoliticalView.query.all()
    political_view = []

    for curr_pol_view in political_views:
        political_view.append((curr_pol_view.political_view_id,
                               curr_pol_view.political_view_name))

    return ["Political ideology", political_view]


def all_religions():
    """ Queries the religions table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    religions = Religion.query.all()
    rel = []

    for religion in religions:
        rel.append((religion.religion_id,
                               religion.religion_name))

    return ["Religious ideology", rel]


def all_outdoors():
    """ Queries the outdoors table.
        Returns a list of tuples, first element is the genre id and second
        element is the name.
        OUTPUT FORMAT = List of tuples(integer, string).
    """

    all_outdoors = Outdoor.query.all()
    activities = []

    for out in all_outdoors:
        activities.append((out.outdoor_id,
                               out.outdoor_activity))

    return ["Favorite Outdoor activity", activities]


def get_user_interests(user_id):
    """ Queries the user_interests table and accepts a userid as input.
        INPUT FORMAT = Integer.
        Returns an object of the type user interest.
        OUTPUT FORMAT = object.
    """

    user = Interest.query.filter(Interest.user_id == user_id).first()
    return user


def get_interest_name(interest_id, table_name):
    """ Queries the given table, accepts interest_id and name of table as
        a parameter.
        INPUT FORMAT = (Integer, string)
        Returns an object of the type interest.
        OUTPUT FORMAT = object.
    """

    Interest = table_name.query.filter(Interest.user_id == user_id).first()


def get_interest_info(interest_info):
    """ Accepts a SINGLE tuple of INPUT FORMAT: (int, int)
        The first element of the tuple is the value of the interest.
        The second element is the table id.
        Assigns the queries to a small dictionary in this order:
            user.interest_id          |(0)
            user.book_genre_id        |(1)
            user.movie_genre_id       |(2)
            user.music_genre_id       |(3)
            user.food_habit_id        |(4)
            user.fav_cuisine_id       |(5)
            user.hobby_id             |(6)
            user.political_view_id    |(7)
            user.religion_id          |(8)
            user.outdoor_id           |(9)
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
    """ Queries the user_matches table and accepts a user id as input.
        INPUT FORMAT = Integer.
        Returns a list of confirm matches for the specific user.
        OUTPUT FORMAT = List of match objects.
    """

    q1 = UserMatch.query
    fil = q1.filter(UserMatch.user_id_2 == 339, UserMatch.user_2_status == False).all()


def update_matched(user_id1, user_id2, query_time):
    """ Accepts 2 user ids as an input.
        user_id1 is the logged in user.
        user_id2 is the user choice.
        INPUT FORMAT = (Integer, Integer, string(Y-m-d H:M:S).
        Checks UserMatch table for a pending match.
        Returns True if a match is made.
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
    """ Queries the pending_match for pending matches.
        user_id = Integer.
        pincode = Integer.
        query_time = String.
        INPUT FORMAT : 399, 95134,"2018-02-28 20:30:00").
        returns a list of pending match user user_ids.
        OUTPUT FORMAT : List of intergers.
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

"""Coffee_buddy."""

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename
from models import *
from queries import *
from matchmaker import *
from yelper import filter_response
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/user_profile_pictures'
# Flask sessions and the debug toolbar
app.secret_key = "ABC"

# this will throw an error if a jinja variable is undefined
app.jinja_env.undefined = StrictUndefined


###############################################################################

@app.route('/')
def index():
    """ This route
    - works as an index with links to every page
    """

    return render_template('index.html')

@app.route('/homepage')
def show_home_page():
    """ This route
    - shows the homepage with links for login and registration
    """

    return render_template("homepage.html")


@app.route('/login', methods=["GET"])
def login_input():
    """For user to login with email"""

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def check_login():
    """Check user login info"""

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter(User.email == email).first()

    if not user:
        flash('Please register your account')
        return redirect('/register')
    elif email == user.email and password == user.password:
        session['user_id'] = user.user_id
        flash('You successfully logged in')
        return redirect('/plan_trip')


@app.route('/register', methods=["GET"])
def register_form():
    """This route
    - Checks theFor user to register with email"""

    all_interests = [all_book_genres(), all_movie_genres(),
                     all_music_genres(), all_food_habits(),
                     all_fav_cuisines(), all_hobbies(),
                     all_political_views(), all_religions(),
                     all_outdoors()]

    return render_template('register.html',
                                all_interests=all_interests)


@app.route('/register', methods=["POST"])
def register_process():
    """This route
    - Gets a new user to register to the db cb
    """

    fname = request.form.get('fname')
    fname = fname.capitalize()
    lname = request.form.get('lname')
    lname = lname.capitalize()
    email = request.form.get('email')
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    date_of_birth = request.form.get('date_of_birth')
    zipcode = request.form.get('zipcode')
    phone = request.form.get('phone')
    one_word = request.form.get('one_word')
    book_genre_id = request.form.get('Preferred book genre')
    movie_genre_id = request.form.get('Preferred movie genre')
    music_genre_id = request.form.get('Preferred music genre')
    food_habit_id = request.form.get('Food habits')
    fav_cuisine_id = request.form.get('Preferred cuisine type')
    hobby_id = request.form.get('Favorite hobby')
    political_view_id = request.form.get('Political ideology')
    religion_id = request.form.get('Religious ideology')
    file = request.files.get('profile_picture', None)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    profile_picture = 'static/user_profile_pictures/' + str(filename)
    outdoor_id = request.form.get('Favorite Outdoor activity')

    user = db.session.query(User).filter(User.email == email).first()

    if not user:
        # if the user does not exist then we instantiate a user and the info
        #to the db
        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    user_name=user_name,
                    password=password,
                    date_of_birth=date_of_birth,
                    zipcode=zipcode,
                    phone=phone,
                    one_word=one_word,
                    profile_picture=profile_picture)


        db.session.add(user)
        db.session.commit()
        userid = user.user_id

        #update user interests for the specific user
        interest = Interest(
                    user_id=userid,
                    book_genre_id=book_genre_id,
                    movie_genre_id=movie_genre_id,
                    music_genre_id=music_genre_id,
                    food_habit_id=food_habit_id,
                    fav_cuisine_id=fav_cuisine_id,
                    hobby_id=hobby_id,
                    political_view_id=political_view_id,
                    religion_id=religion_id,
                    outdoor_id=outdoor_id
                    )

        db.session.add(interest)
        db.session.commit()

    session['user_id'] = user.user_id
    flash('You are successfully registerd and logged in')
    return redirect('/plan_trip')


@app.route('/user_info', methods=["GET"])
@login_req
def show_profile():
    """show the user their own profile"""

    userid = session.get("user_id")

    user_info = get_user_info(userid)

    return render_template('/user_info.html',user_info=user_info)


@app.route('/plan_trip', methods=["GET"])
@login_req
def show_map():
    """This route
    - Uses the pincode from the session to render a map
    - Shows a map with coffeeshops
    """

    return render_template("/plan_trip.html")


@app.route('/plan_trip', methods=["POST"])
@login_req
def plan_trip():
    """This route
    - gets the trip time from the user who is logged in
    - gets the trip pincode from the user
    """

    query_time = request.form.get('triptime')
    query_pin_code = request.form.get('pincode')
    user_id = session['user_id']
    session['query_pincode'] = query_pin_code

    #add user query to the db

    trip =  PendingMatch(user_id=user_id,
                        query_pin_code=query_pin_code,
                        query_time=query_time,
                        pending=True)

    db.session.add(trip)
    db.session.commit()

    #at this point we will pass the information the yelper
    #yelper will end information to google and google will render
    # a map with relevant information

    return redirect("/show_matches")


@app.route('/show_matches',methods=['GET'])
@login_req
def show_potenital_matches():
    """ This route
        - accesses the session for a user_id and query_pin_code
        - accesses the matchmaker module for making matches
        -
    """
    # gets the user_id from the session
    userid = session.get('user_id')
    # gets the pincode from the session
    pin = session.get('query_pincode')
    # gets a list of pending matches using the potential_matches from
    # the matchmaker module
    # potential_matches is  a list of user_ids
    # => [189, 181, 345, 282, 353, 271, 9, 9, 501, 9]
    potential_matches = query_pending_match(pin)
    # gets a list of tuples of match percents for the userid
    # uses the create_matches from the matchmaker
    # create_matches takes a list of user_ids as the first param
    # create_matches take the userid as the second param
    # create_matches([30,40,50],60)
    # => [(60, 30, 57.90407177363699), (60, 40, 54.887163561076605)]
    match_percents = create_matches(potential_matches, userid)

    user_info = get_user_info(userid)
    # this is the logged in user's info
    user_name = get_user_name(userid)
    # this is the logged in user's username

    match_info = []

    for user in match_percents:
        username = get_user_name(user[1])
        matched_user_id = user[1]
        matched_username = username[0] + " " + username[1]
        match_percent = round(user[2])

        match_info.append((matched_username, match_percent, matched_user_id))

    # match info is a list of tuples [(username,
    #                               match_percent,
    #                               matched_user_id)]
    return render_template('show_matches.html',
                                user_name=user_name,
                                user_info=user_info,
                                match_info=match_info)


@app.route('/show_matches',methods=["POST"])
@login_req
def update_potenital_matches():
    """ This route
        - Gets the user input for a confirm match
        - Updates the user input for a match to the db
    """

    matched = request.form.get("user_match")
    user_id_1 = session['user_id']
    match_date = datetime.datetime.now()
    query_pincode = session['query_pincode']

    match = UserMatch(user_id_1=user_id_1,
                    user_id_2=matched,
                    match_date=match_date,
                    user_2_status=bool("False"),
                    query_pincode=query_pincode)

    db.session.add(match)
    db.session.commit()

    return redirect()


@app.route('/show_match_details', methods=["GET"])
@login_req
def show_match_details():
    """ This function
        - displays the final match of user's choice
        - shows all the common interests to the user
        - gives the user a chance to message the match
        - gives the user a chance to choose a coffee shop
    """


    pass

@app.route('/show_map', methods=["GET"])
@login_req
def choose_coffee_shop():
    """ This function
        - Displays a map with reccomended coffee shops
        - Displays a map with pointers for the user's chosen pincode
    """
    return render_template('map.html')


@app.route("/coffee-info.json")
@login_req
def melon_info():
    """ This function
        - Returns information about coffee shops as JSON.
    """

    # gets the the pincode from the session
    pin = session.get('query_pincode')
    # calls filter response from yelper module
    reccomendations = filter_response(pin)
    # passes the json to the caller
    return jsonify(reccomendations)


@app.route('/logout')
def log_out_user():
    """ This function
        -empties the session to make sure that the user is logged out
    """

    session["user_id"] = None
    session["query_pincode"] = None

    return render_template('logout.html')

##############################################################################


if __name__ == "__main__":
    # Sets debug=True here, since it has to be True at the
    # point that invokes the DebugToolbarExtension
    app.debug = True
    # Makes sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    # Uses the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')

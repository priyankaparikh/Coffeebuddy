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
# app.jinja_env.undefined = StrictUndefined


###############################################################################

@app.route('/')
def show_home_page():
    """ Shows the homepage with links for login and registration.
    """
    return render_template("homepage.html")


@app.route('/login', methods=["GET"])
def login_input():
    """For user to login with email"""
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def check_login():
    """Check user login info."""

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter(User.email == email).first()

    if not user:
        flash('Please register your account')
        return redirect('/register')
    elif email == user.email and password == user.password:
        session['user_id'] = user.user_id
        flash('You successfully logged in')
        return redirect('/user_info')
    else:
        flash('Oops looks like you have entered the wrong password.Please re-enter your login information')
        return redirect('login')


@app.route('/register', methods=["GET"])
def register_form():
    """ Displays the registeration form to the User."""

    all_interests = [all_book_genres(), all_movie_genres(),
                     all_music_genres(), all_food_habits(),
                     all_fav_cuisines(), all_hobbies(),
                     all_political_views(), all_religions(),
                     all_outdoors()]

    return render_template('register2.html',
                                all_interests=all_interests)


@app.route('/register', methods=["POST"])
def register_process():
    """ Gets user data from the front end and validates a registration.
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

    user = db.session.query(User).filter(User.email == email,
                            User.date_of_birth == date_of_birth).first()

    if not user:
        # if the user does not exist then instantiate a user and the info
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
        return redirect('/user_info')

    elif user:
        flash('Looks like you are already a registered user. Please log in to plan a trip.')
        return redirect('')


@app.route('/user_info', methods=["GET"])
@login_req
def show_profile():
    """show the user their own profile.

    user_info = get_user_info(251)
    [251, u'JamesFuentes@fastmail.com', u'JeFns', u'1998-02-16',
    u'08707', u'(074)590-8409x0046', u'James', u'Fuentes',
    u'/static/user_profile_pictures/pexels-photo-354951.jpeg']
    """

    userid = session.get("user_id")

    user_info = get_user_info(userid)
    user_interest_info = get_interest_display(userid)
    all_matches = get_all_made_matches(userid)
    all_trips = find_trip_count(userid)

    return render_template('/user_info.html',user_info=user_info,
                            user_interest_info=user_interest_info,
                            all_matches=all_matches, all_trips=all_trips)


@app.route("/user_profile/<user_id>", methods=["POST"])
@login_req
def show_match_profile(user_id):
    """Return page showing the details of a given user_profile.
    """

    userid = request.form.get("match_profile")
    user_interests = get_interest_display(userid)
    user_info = get_user_info(userid)

    return render_template('/match_profile2.html',user_info=user_info,
                                                user_interests=user_interests)


@app.route('/plan_trip', methods=["GET"])
@login_req
def show_map():
    """Route for users to plan a trip.

    - Uses the pincode from the session to render a map
    - Shows a map with coffeeshops
    """

    return render_template("/plan_trip2.html")


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
    session_time = clean_time(query_time)
    session['query_time'] = session_time

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
def show_potential_matches():
    """ This route
        - accesses the session for a user_id and query_pin_code
        - accesses the matchmaker module for making matches
        -
    """
    # gets the user_id from the session
    userid = session.get('user_id')
    # gets the pincode from the session
    pin = session.get('query_pincode')
    # gets the query_time from the session
    query_time = session.get('query_time')
    # gets a list of pending matches using the potential_matches from
    # the matchmaker module
    # potential_matches is  a list of user_ids
    # => [189, 181, 345, 282, 353, 271, 9, 9, 501, 9]
    potential_matches = find_valid_matches(userid, pin, query_time)
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
        user_info = get_user_info(user[1])
        matched_user_id = user[1]
        matched_username = username[0] + " " + username[1]
        match_percent = round(user[2])
        match_details = get_commons(user[1], userid)

        match_info.append((matched_username, match_percent,
                        matched_user_id, user_info, match_details))

    # match info is a list of tuples [(username,
    #                               match_percent,
    #                               matched_user_id,
    #                                user_info, match_details)]

    return render_template('show_matches.html',
                                user_name=user_name,
                                user_info=user_info,
                                match_info=match_info)


@app.route('/show_matches',methods=["POST"])
@login_req
def update_potential_matches():
    """ This route
        - Gets the user input for a confirm match
        - Updates the user input for a match to the db
    """

    matched = request.form.get("user_match")
    user_id_1 = session['user_id']
    match_date = datetime.datetime.now()
    query_pincode = session['query_pincode']
    session['matched_user'] = matched

    match = UserMatch(user_id_1=user_id_1,
                    user_id_2=matched,
                    match_date=match_date,
                    user_2_status=False,
                    query_pincode=query_pincode)

    db.session.add(match)
    db.session.commit()
    return redirect('/show_map')

@app.route('/show_match_details', methods=["POST"])
@login_req
def show_match_details():
    """ This route
        - displays the final match of user's choice
        - shows all the common interests to the user
        - gives the user a chance to message the match
        - gives the user a chance to choose a coffee shop
    """

    userid1 = session["user_id"]
    userid2 = request.form.get("match_details")
    user_info1 = get_user_info(userid1)
    username_1 = get_user_name(userid1)
    username1 = username_1[0] + " " + username_1[1]
    user_info2 = get_user_info(userid2)
    username_2 = get_user_name(userid2)
    username2 = username_2[0] + " " + username_2[1]
    match_info = get_commons(userid1, userid2)
    match_percent = round(make_match(userid1, userid2))

    return render_template("match_console.html", user_info1=user_info1,
                                                    username1=username1,
                                                    username2=username2,
                                                    user_info2=user_info2,
                                                    match_info=match_info,
                                                    match_percent=match_percent)

@app.route('/show_map', methods=["GET"])
@login_req
def show_coffee_shop():
    """ This route
        - Displays a map with reccomended coffee shops
        - Displays a map with pointers for the user's chosen pincode
    """
    matched_username = get_user_name(session['matched_user'])

    return render_template('map.html', matched_username=matched_username)


@app.route('/show_map', methods=["POST"])
@login_req
def invite_user():
    """This route
        - accepts input from a map
        - sends a text message to a matched user
    """

    return render_template('send_message.html')

@app.route("/coffee-info.json")
@login_req
def coffee_info():
    """ This function
        - Returns information of latlong for coffee shops as JSON.

        reccomendations = [
           {lat: 52.511, lng: 13.447, info: info},
           {lat: 52.549, lng: 13.422, info: info},
           {lat: 52.497, lng: 13.396, info: info},
           {lat: 52.517, lng: 13.394, info: info}
         ];
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

    session['matched_user'] = None
    session['user_id'] = None
    session['query_time'] = None
    session['query_pincode'] = None

    return render_template('logout.html')

##############################################################################


if __name__ == "__main__":
    # Sets debug=True here, since it has to be True at the
    # point that invokes the DebugToolbarExtension
    app.debug = False
    # Makes sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    # Uses the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')

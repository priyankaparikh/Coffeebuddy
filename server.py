"""Coffee_buddy"""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from models import *
from queries import *

app = Flask(__name__)

# Flask sessions and the debug toolbar
app.secret_key = "ABC"

# this will throw an error if a jinja variable is undefined
app.jinja_env.undefined = StrictUndefined


###################################################################################################################

@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')

@app.route('/login', methods=["GET"])
def login_input():
    """For user to login with email"""

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def check_login():
    """Check user login info"""
    
    email = request.form.get('email')
    password = request.form.get('password')

    check_db = db.session.query(User).filter(User.email == email)
    #User.password == password
    user = check_db.first()

    if not user:
        flash('Please register your account')
        return redirect('/register')
    elif email == User.email and password == User.password:
        session['user_id'] = user.user_id
        flash('You successfully logged in')
        return redirect('/users/' + str(user.user_id))
    else:
        return redirect('/forgot_password')


@app.route('/register', methods=["GET"])
def register_form():
    """For user to register with email"""

    all_interests = [all_book_genres(), all_movie_genres(),
                     all_music_genres(), all_food_habits(),
                     all_fav_cuisines(), all_hobbies(),
                     all_political_views(), all_religions(),
                     all_outdoors()]

    return render_template('register.html',
                                all_interests=all_interests)


@app.route('/register', methods=["POST"])
def register_process():
    """Get user registration and redirect to user_interests"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    date_of_birth = request.form.get('date_of_birth')
    zipcode = request.form.get('zipcode')
    phone = request.form.get('phone')
    one_word = request.form.get('one_word')
    book_genre_id = request.form.get('Preferred book')
    movie_genre_id = request.form.get('Preferred movie genre')
    music_genre_id = request.form.get('Preferred music genre')
    food_habit_id = request.form.get('Food habits')
    fav_cuisine_id = request.form.get('Preferred cuisine type')
    hobby_id = request.form.get('Favorite hobby')
    political_view_id = request.form.get('Political ideology')
    religion_id = request.form.get('Religious ideology')
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
                    one_word=one_word
                    )


        db.session.add(user)
        db.session.commit()

        interest = Interest(
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
    

@app.route('/user_info', methods=["GET"])
def show_profile():
    """show the user thier own profile"""

    user_info = get_user_info("20")

    return render_template('/user_info.html',user_info=user_info)


@app.route('/plan_trip', methods=["GET"])
def show_map():
    """Show a map with coffeeshops"""

    return render_template("/plan_trip.html")


@app.route('/plan_trip', methods=["POST"])
def plan_trip():
    """get trip time, pincode"""

    time = request.form.get('time')
    pincode = request.form.get('pincode')

    #at this point we will pass the information the yelper
    #yelper will end information to google and google will render
    # a map with relevant information
    
    return render_template('map.html', time=time, pincode=pincode)

@app.route('/show_map', methods=["GET"])
def choose_coffee_shop():
    """get user query"""
    

    return render_template('map.html')



###################################################################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from models import connect_to_db, db
from server import app
from models import User
from faker import Faker

def load_users():
    """Load users from static/user_data.txt into database."""

    print "Users"
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/user_data.txt")
        row = row.rstrip()
        #is this pythonic ?
        fname, lname, email, user_name, password, date_of_birth, zipcode, phone ,one_word = row.split("|")

        user = User(fname=fname,
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


def load_user_interests():



def load_movies():
    """Load movies from u.item into database."""


def load_ratings():
    """Load ratings from u.data into database."""


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()

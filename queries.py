"""test the models for database querys"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import * 

####################################################################
def get_user_id(input_email):
    """return the only user_id of a user

    >>> get_user_id('LeahChavez@gmail.com')
    489
    """

    user = User.query.filter(User.email == '{}'.format(input_email)).all()

    # at this point our user looks something like this :
    #[<user_id=489, email=LeahChavez@gmail.com, user_name=LhCv, password=bZ@KRW@k+4,
    #date_of_birth=1983-04-29, zipcode=24568, phone=+96(5)2036281580>]

    user_id = user[0].user_id

    return user_id


def get_user_info(input_id):
    """return user_info as a list using the user_id

    >>> get_user_info('280')
    [280, u'EricaBrown@fastmail.com', u'EcBw', u'1990-01-13', u'27359', u'+47(7)9589562562']
    
    """

    user = User.query.filter(User.user_id == '{}'.format(input_id)).all()

    user_id = user[0].user_id
    email = user[0].email
    user_name = user[0].user_name
    date_of_birth = user[0].date_of_birth
    zipcode = user[0].zipcode
    phone = user[0].phone

    return [user_id, email, user_name, date_of_birth, zipcode, phone]

def validate_password(input_email, input_password):
    """check if an email and password are valid"""

    user = User.query.filter(User.email == '{}'.format(input_email)).first()
    password = user[0].password
    email = user[0].email

    return password == input_password and email == input_email




def get_user_interest(user_id):
    """return all the interests of a user using the user_id"""
    
def all_book_genres():
    """returns a list of tuples with book genre ids and book genres"""

def all_movie_genres():
    """returns a list of tuples with book genre ids and book genres"""

def all_book_genres():
    """returns a list of tuples with book genre ids and book genres"""

def query_matched(user_id):
    """return all the made matches in the history of the user"""

def update_user_info(info):
    """dynamically updates user_information by checking the data type of the input"""





#####################################################################
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    db.create_all()
    import doctest

    result = doctest.testmod()
    if not result.failed:
        print("All tests passed!")

    print "Connected to DB."
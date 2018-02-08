"""test the models for database querys"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import * 

####################################################################
def query_user_id(email):
    """return the user_id of a user for ruther_queries"""

def query_user_infor(user_id):
    """return user_info using the user_id"""

def query_user_interest(user_id):
    """return all the interests of a user using the user_id"""

def query_matched(user_id):
    """return all the made matches in the history of the user"""

def update_user_info(info):
    """dynamically updates user_information by checking the data type of the input"""
    
    user_input = info





#####################################################################
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
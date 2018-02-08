from sqlalchemy import func
from models import connect_to_db, db
from models import *
from sqlalchemy import inspect

##############################################################################################
"""this Test queries the current database and checks if all the values have loaded"""

def check_db():
    """check if there is even a db"""


def check_user():
    """check if User table has any users"""


def check_interest():
    """check if Interest table has any interests"""


def check_bookgenre():
    """check if Book genres loaded correctly"""


def check_moviegenre():
    """check if Movie genres loaded correctly"""


def check_musicgenre():
    """check if Music genres loaded correctly"""


def check_foodhabit():
    """check if the food habits loaded correctly"""


def check_favcuisine():
    """check if fav cuisines loaded correctly"""


def check_hobbies():
    """check if hobbies loaded correctly"""


def check_religion():
    """check if religion loaded correctly"""


def check_political_views():
    """check if political views loaded correctly"""


def check_outdoor():
    """check if outdoor loaded correctly"""





########################################################################################################

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    db.create_all()

check_db()
check_user()  
check_interest()
check_bookgenre()
check_moviegenre()
check_musicgenre()
check_foodhabit()
check_favcuisine()
check_hobbies()
check_religion()
check_political_views()
check_outdoor()

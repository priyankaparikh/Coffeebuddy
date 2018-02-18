from sqlalchemy import func
from models import * 
from queries import get_user_interests, query_pending_match

"""this module returns a match percentage for two specific users when their user_interests
    are passed through the function
    
    we are passing something that looks like this from the queries module 
    call the query_pending_matches() 
    pass the value into get_user_interests()

    the value returned by get_user_interests()
    [(189, [< interest_id=189, book_genre_id=22, movie_genre_id=4, music_genre_id=10, 
    food_habit_id=2, fav_cuisine_id=4, hobby_id=8, politicial_view_id=4, religion_id=4, 
    outdoor_id=8>]), 
    (181, [< interest_id=181, book_genre_id=4, movie_genre_id=16, 
    music_genre_id=10, food_habit_id=3, fav_cuisine_id=10, hobby_id=13, politicial_view_id=3,
    religion_id=4, outdoor_id=7>]), 
    (345, [< interest_id=345, book_genre_id=24, 
    movie_genre_id=20, music_genre_id=19, food_habit_id=4, fav_cuisine_id=14, hobby_id=1,
    politicial_view_id=4, religion_id=2, outdoor_id=8>]), 
    (282, [< interest_id=282,
    book_genre_id=6, movie_genre_id=4, music_genre_id=18, food_habit_id=4, fav_cuisine_id=1, 
    hobby_id=16, politicial_view_id=3, religion_id=1, outdoor_id=10>]), 
    (353, [< interest_id=353,
    book_genre_id=20, movie_genre_id=18, music_genre_id=8, food_habit_id=4, 
    fav_cuisine_id=3, hobby_id=15, politicial_view_id=2, religion_id=7, outdoor_id=6>]), 
    (271, [< interest_id=271, book_genre_id=19, movie_genre_id=23, music_genre_id=7, food_habit_id=4, 
    fav_cuisine_id=2, hobby_id=9, politicial_view_id=3, religion_id=5, outdoor_id=5>])]

        book_genre = 8pts           |    6
        movie_genre = 6pts          |    8
        music_genre = 9pts          |    5
        food_habit = 13pts          |    4
        fav_cuisine = 7pts          |    7
        hobby = 5pts                |    9
        political_view = 20pts      |    1
        religious_view = 17pts      |    2
        outdoor = 15pts             |    3

    """
#######################################################################################################

def extract_vals(user):
    """return a list of values for each user's interest_id"""

    required_values = []

    required_values.append(user.interest_id)
    required_values.append(user.book_genre_id)
    required_values.append(user.movie_genre_id)
    required_values.append(user.music_genre_id)
    required_values.append(user.food_habit_id)
    required_values.append(user.fav_cuisine_id)
    required_values.append(user.hobby_id)
    required_values.append(user.political_view_id)
    required_values.append(user.religion_id)
    required_values.append(user.outdoor_id)

    return required_values


def calculate_coeffecient(similarity_diff, max_id, point_values):
    """ returns a % for a specific quality"""
    return ((max_id - similarity_diff) / float(max_id)) * point_values


def make_match(user_id_1, user_id_2):
    """return a percentage of the user matches
    """
    match_total = 0

    user_1_interests = get_user_interests(user_id_1)
    user_2_interests = get_user_interests(user_id_2)

    vals1 = extract_vals(user_1_interests)
    vals2 = extract_vals(user_2_interests)

    if len(vals1) == len(vals2):
        #vals1[0] and vals2[0] are the user_interest_ids
        max_book_genre_id = db.session.query(func.max(BookGenre.book_genre_id)).one()
        max_book_id = int(max_book_genre_id[0])
        user_1_book_genre_id = vals1[1]
        user_2_book_genre_id = vals2[1]
        diff1 = abs(user_1_book_genre_id - user_2_book_genre_id)
        book_match = calculate_coeffecient(diff1, max_book_id, 6)
        match_total += book_match
        
        max_movie_genre_id = db.session.query(func.max(MovieGenre.movie_genre_id)).one()
        max_movie_id = int(max_movie_genre_id[0])
        user_1_movie_genre_id = vals1[2]
        user_2_movie_genre_id = vals2[2]
        diff2 = abs(user_1_movie_genre_id - user_2_movie_genre_id)
        movie_match = calculate_coeffecient(diff2, max_movie_id, 8)
        match_total += movie_match

        max_music_genre_id = db.session.query(func.max(MusicGenre.music_genre_id)).one()
        max_music_id = int(max_music_genre_id[0])
        user_1_music_genre_id = vals1[3]
        user_2_music_genre_id = vals2[3]
        diff3 = abs(user_1_music_genre_id - user_2_music_genre_id)
        music_match = calculate_coeffecient(diff3, max_music_id, 5)
        match_total += music_match

        max_food_habit_id = db.session.query(func.max(FoodHabit.food_habit_id)).one()
        max_food_habit = int(max_food_habit_id[0])
        user_1_food_habit_id = vals1[4]
        user_2_food_habit_id = vals2[4]
        diff4 = abs(user_1_food_habit_id - user_2_food_habit_id)
        food_habit_match = calculate_coeffecient(diff4, max_food_habit, 13)
        match_total += food_habit_match

        max_fav_cuisine_id = db.session.query(func.max(FavCuisine.fav_cuisine_id)).one()
        max_fav_cuisine = int(max_fav_cuisine_id[0])
        user_1_fav_cuisine_id = vals1[5]
        user_2_fav_cuisine_id = vals2[5]
        diff5 = abs(user_1_fav_cuisine_id - user_2_fav_cuisine_id)
        fav_cuisine_match = calculate_coeffecient(diff5, max_fav_cuisine, 7)
        match_total += fav_cuisine_match

        max_hobby_id = db.session.query(func.max(Hobby.hobby_id)).one()
        max_hobby = int(max_hobby_id[0])
        user_1_hobby_id = vals1[6]
        user_2_hobby_id = vals2[6]
        diff6 = abs(user_1_hobby_id - user_2_hobby_id)
        hobby_match = calculate_coeffecient(diff6, max_hobby, 5)
        match_total += hobby_match

        max_political_view_id = db.session.query(func.max(PoliticalView.political_view_id)).one()
        max_political_view = int(max_political_view_id[0])
        user_1_political_view_id = vals1[7]
        user_2_political_view_id = vals2[7]
        diff7 = abs(user_1_political_view_id - user_2_political_view_id)
        political_match = calculate_coeffecient(diff7, max_political_view, 20)
        match_total += political_match

        max_religion_id = db.session.query(func.max(Religion.religion_id)).one()
        max_religion = int(max_religion_id[0])
        user_1_religion_id = vals1[8]
        user_2_religion_id = vals2[8]
        diff8 = abs(user_1_religion_id - user_2_religion_id)
        religion_match = calculate_coeffecient(diff8, max_religion, 17)
        match_total += religion_match

        max_outdoor_id = db.session.query(func.max(Outdoor.outdoor_id)).one()
        max_outdoor = int(max_outdoor_id[0])
        user_1_outdoor_id = vals1[9]
        user_2_outdoor_id = vals2[9]
        diff9 = abs(user_1_outdoor_id - user_2_outdoor_id)
        outdoor_match = calculate_coeffecient(diff9, max_outdoor, 15)
        match_total += outdoor_match

       
    return match_total
    

def create_matches(potential_matches, user1):
    """accepts a list of user_id's with similar queries and returns a list of tuples
    """
    matched = []

    for user in potential_matches:
        if user1 != user :
            match_percent = make_match(user1, user)
            matched.append((user1, user, match_percent))

    return matched


########################################################################################################
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB"


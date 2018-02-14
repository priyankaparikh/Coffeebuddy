""" this module returns a match percentage for two specific users when their user_interests
    are passed through the function
    
    we are passing something that looks like this from the queries module 
    call the query_pending_matches() 
    pass the value into get_user_interests()

    the value returned by get_user_interests()
    [(189, [< interest_id=189, book_genre_id=22, movie_genre_id=4, music_genre_id=10, 
    food_habit_id=2, fav_cuisine_id=4, hobby_id=8, politicial_view_id=4, religion_id=4, 
    outdoor_id=8>]), (181, [< interest_id=181, book_genre_id=4, movie_genre_id=16, 
    music_genre_id=10, food_habit_id=3, fav_cuisine_id=10, hobby_id=13, politicial_view_id=3,
    religion_id=4, outdoor_id=7>]), (345, [< interest_id=345, book_genre_id=24, 
    movie_genre_id=20, music_genre_id=19, food_habit_id=4, fav_cuisine_id=14, hobby_id=1,
    politicial_view_id=4, religion_id=2, outdoor_id=8>]), (282, [< interest_id=282,
    book_genre_id=6, movie_genre_id=4, music_genre_id=18, food_habit_id=4, fav_cuisine_id=1, 
    hobby_id=16, politicial_view_id=3, religion_id=1, outdoor_id=10>]), (353, [< interest_id=353,
    book_genre_id=20, movie_genre_id=18, music_genre_id=8, food_habit_id=4, 
    fav_cuisine_id=3, hobby_id=15, politicial_view_id=2, religion_id=7, outdoor_id=6>]), 
    (271, [< interest_id=271, book_genre_id=19, movie_genre_id=23, music_genre_id=7, food_habit_id=4, 
    fav_cuisine_id=2, hobby_id=9, politicial_view_id=3, religion_id=5, outdoor_id=5>])]

     book_genre = 8pts
        movie_genre = 6pts
        music_genre = 9pts
        food_habit = 13pts
        fav_cuisine = 7pts
        hobby = 5pts
        political_view = 20pts
        religiouse_view = 17pts
        outdoor = 15pts

    """
#######################################################################################################

def extract_vals(user):
    """return a list of values for each user's interest_id"""

    interest_id = user.interest_id
    book_genre_id = user.book_genre_id
    movie_genre_id = user.movie_genre_id
    music_genre_id = user.music_genre_id
    food_habit_id = user.food_habit_id
    fav_cuisine_id = user.fav_cuisine_id
    hobby_id = user.hobby_id
    politicial_view_id = user.politicial_view_id
    religion_id = user.religion_id
    outdoor_id = user.outdoor_id


    return [interest_id, book_genre_id, movie_genre_id, music_genre_id, food_habit_id, fav_cuisine_id, hobby_id, political_view,religion_id, outdoor_id]

def make_match(users):
    """return a percentage of the user matches
    """

    for user in users:




def calculate_coeffecient(similarity_diff, max_id, point_values):
    """ returns a % for a specific quality
    """

    return ( similarity_diff / max_id ) * point_values






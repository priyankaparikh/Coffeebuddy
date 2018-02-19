from faker import Faker
import random
fake = Faker()
import os

def generate_users(n):
    """generates a bunch of users and user info for data files"""

    email_providers = ['gmail','yahoo','aol','hotmail','fastmail']
    profile_pics = ['/static/user_profile_pictures/pexels-photo-206445.jpeg',
                '/static/user_profile_pictures/pexels-photo-720606.jpeg',
                '/static/user_profile_pictures/pexels-photo-211050.jpeg',
                '/static/user_profile_pictures/pexels-photo-428333.jpeg',  
                '/static/user_profile_pictures/pexels-photo-734168.jpeg',
                '/static/user_profile_pictures/pexels-photo-220453.jpeg',
                '/static/user_profile_pictures/pexels-photo-450271.jpeg', 
                '/static/user_profile_pictures/pexels-photo-736716.jpeg',
                '/static/user_profile_pictures/pexels-photo-227294.jpeg',
                '/static/user_profile_pictures/pexels-photo-539727.jpeg',
                '/static/user_profile_pictures/pexels-photo-756453.jpeg',
                '/static/user_profile_pictures/pexels-photo-235531.jpeg',
                '/static/user_profile_pictures/pexels-photo-567459.jpeg',
                '/static/user_profile_pictures/pexels-photo-762020.jpeg',
                '/static/user_profile_pictures/pexels-photo-237593.jpeg',
                '/static/user_profile_pictures/pexels-photo-58021.jpeg',  
                '/static/user_profile_pictures/pexels-photo-769746.jpeg',
                '/static/user_profile_pictures/pexels-photo-295564.jpeg',
                '/static/user_profile_pictures/pexels-photo-634030.jpeg',
                '/static/user_profile_pictures/pexels-photo-774909.jpeg',
                '/static/user_profile_pictures/pexels-photo-325682.jpeg',
                '/static/user_profile_pictures/pexels-photo-681793.jpeg',
                '/static/user_profile_pictures/pexels-photo-91227.jpeg',
                '/static/user_profile_pictures/pexels-photo-354951.jpeg',
                '/static/user_profile_pictures/pexels-photo-705821.jpeg', 
                '/static/user_profile_pictures/pexels-photo-355164.jpeg',
                '/static/user_profile_pictures/pexels-photo-712513.jpeg']

    text_file = open('seed_data/user_data.txt', 'w')

    for i in range(1, n):
        user_id = i
        fname = fake.first_name()
        lname = fake.last_name()
        email = fname + lname + '@' + random.choice(email_providers) + '.com'
        user_name = fname[::3] + lname[::3]
        password = fake.password()
        date_of_birth = fake.date_between(start_date='-40y', end_date='-16y')
        zipcode = fake.zipcode()
        phone = fake.phone_number()
        one_word = fake.word(ext_word_list=None)
        profile_picture = random.choice(profile_pics) 
        data1 = str(i) + '|' + fname + '|' + lname + '|' + email + '|' + user_name + '|' + password 
        data2 = '|' + str(date_of_birth) + '|' + zipcode + '|' + phone + '|' + one_word + '|' + profile_picture
        data = data1 + data2 + '\n'
        text_file.write(data)
        print data 

    text_file.close()

def generate_user_queries(n):
    """ generates a bunch of user_queries for the user_data queries file"""

    pincodes = ['95134', '95111', '98145', '98164', '97639']
    text_file = open('seed_data/pending_match_data.txt', 'w')

    for i in range(1, n):
        user_id = random.randrange(1, 498)
        query_pin_code = random.choice(pincodes)
        pending = 'True'

        data = str(user_id) + '|' + query_pin_code + '|'+ pending +'\n'
    
        text_file.write(data)

    text_file.close()


def generate_user_profile_pics():
    """ generates the names of pics from the static folder and writes it to the 
    open file"""

    a = open("seed_data/user_profile_pic_data.txt", "w")
    for path, subdirs, files in os.walk(r'vagrant@vagrant:~/src/coffeebuddy/static/user_profile_pictures'):
        for filename in files:
            f = os.path.join(path, filename)
            a.write(str(f) + os.linesep)

    a.close()


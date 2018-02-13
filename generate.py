from faker import Faker
import random
fake = Faker()

def generate_users(n):
    """generates a bunch of users and user info for data files"""

    email_providers = ['gmail','yahoo','aol','hotmail','fastmail']
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
        data1 = str(i) + '|' + fname + '|' + lname + '|' + email + '|' + user_name + '|' + password 
        data2 = '|' + str(date_of_birth) + '|' + zipcode + '|' + phone + '|' + one_word 
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




from faker import Faker, Hipster
import random
fake = Faker()
text_file = open("seed_data/user_data.txt", "w")

def generate_users(n):
    """generates a bunch of users and user info for data files"""

    email_providers = ['gmail','yahoo','aol','hotmail','fastmail']

    for i in range(1, n + 1):
        fname = fake.first_name()
        lname = fake.last_name()
        email = fname + lname + '@' + random.choice(email_providers) + '.com'
        user_name = fname[::3] + lname[::3]
        password = fake.password()
        date_of_birth = fake.date_between(start_date="-40y", end_date="-16y")
        zipcode = fake.zipcode()
        phone = fake.phone_number()
        one_word = fake.Hipster.word(ext_word_list=None)
        data1 = fname + "|" + lname + "|" + email + "|" + user_name + "|" + password 
        data2 = "|" + str(date_of_birth) + "|" + zipcode + "|" + phone + "|" + one_word + "|"
        data = data1 + data2 + "\n"
        text_file.write(data)
        print data 

    text_file.close()


def generate_interests():
    """ generates data for the user_interest table """

    


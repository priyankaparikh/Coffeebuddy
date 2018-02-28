""" This module enables Users to send free texts to each other.
Uses the Twilio API.
"""
from twilio.rest import Client
import os


def send_message(user_number,user_message):
    """ This function
    - Sends a text to a user using coffeeBuddy's Twilio number.
    - Updates the DB for chat conversations between two users.
    """
    # Account SID from twilio.com/console
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    # Auth Token from twilio.com/console
    auth_token  = os.environ["TWILIO_AUTH_TOKEN"]
    # twilio Number from twilio.com/console
    my_number = os.environ["TWILIO_NUMBER"]

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=str(user_number),
        from_= str(my_number),
        body= str(user_message))

    print(message.sid)

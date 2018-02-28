"""
This Module utilises the Yelp Search Api
- To query for businesses by a search term and location
Using the yelp Business API
- To query additional information about the top result
from the search query.

Functions:
1) request:
    - Creates a url for the server to send yelp.
    - sends a request to the yelp Api.
2) search:
    - Accepts a location as a parameter.
    - Calls the request function.
    - Gets a response JSON from the request function.
3) filter_response:
    - Accepts a location as a parameter.
    - Calls the search function.
    - Parses the return data for relevant CoffeeBuddy information.
"""

import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode
import os

# Yelp uses private keys to authenticate requests (API Key)
# API constants :
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DEFAULT_TERM = 'coffee'
DEFAULT_LOCATION = '95134'
SEARCH_LIMIT = 49 #the limit is 50


def request(host, path, api_key, url_params=None):
    """
    This function
    - Makes a request by formatting query constants
    - creates a url
    - creates a header
    - call for a response from the yelp API_KEY
    Given:
        your API_KEY, send a GET request to the API.
        - host (str): host of the API.
        - path (str): The path of the API
        - API_KEY (str): API Key.
        - url_parmas(dict): query params
    Returns:
        - dict: The JSON response from the request.
    Raises:
        - HTTPError: An error occurs from the HTTP request.
    """

    # url_params is a dict
    # url_params is an optional set of query params in the request
    url_params = url_params or {}
    # encodes the path with utf8 before sending the get request
    # strings over the internet are usually encoded with utf8
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    # adds the api_key to the headers dictionary
    headers = {'Authorization': 'Bearer %s' % api_key}

    print(u'Querying {0} ...'.format(url))
    # sends a get request with : 1) url, 2) headers 3) url_params
    response = requests.request('GET', url, headers=headers, params=url_params)
    # returns the response as a json
    return response.json()


def search(location):
    """
    This function
    - Queries the Search API by a search term and location.
    Parameters:
        - term (str): The search term passed to the API.
        - location (str): The search location passed to the API.
    Returns:
        a list of dictionaries with required info only
    """

    API_KEY= os.environ["YELP_API_KEY"]

    url_params = {
        'term': 'coffee'.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }

    coffee_shop_info = request(API_HOST, SEARCH_PATH, API_KEY, url_params=url_params)

    return coffee_shop_info

def filter_response(pincode):
    """ This function
    - calls the search function for a JSON
    - Parses through the JSON response from the yelp API
        and returns a structure that looks like this:
        var neighborhoods = [
            lat_lng : {lat: 52.511, lng: 13.447},
            business_name : "Peet's Coffee",
            image_url : "image",
            address : "address",
            rating : 4,
            review_count : 144,
            url : business(yelp)URL
        ];
    """

    to_render = []

    pin = str(pincode)
    response = search(pin)
    all_businesses = response['businesses']

    for business in all_businesses:
        lat_lng = {}
        info = {}
        lat_lng['lat'] = business['coordinates']['latitude']
        lat_lng['lng'] = business['coordinates']['longitude']
        info['lat_long'] = lat_lng
        info['business_name'] = business['name']
        info['image_url'] = business['image_url']
        info['address'] = business['location']['display_address']
        info['rating'] = business['rating']
        info['review_count'] = business['review_count']
        info['url'] = business['url']
        to_render.append(info)

    print to_render
    return to_render

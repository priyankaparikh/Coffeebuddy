"""
Using the yelp Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

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


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
DEFAULT_TERM = 'coffee'
DEFAULT_LOCATION = '95134'
SEARCH_LIMIT = 20


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
        host (str): host of the API.
        path (str): The path of the API
        API_KEY (str): API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()



def search(location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
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
    """parses through the json response from yelp
    we want the yelp json to return a structure that looks like this

     var neighborhoods = [
        {lat: 52.511, lng: 13.447},
        {lat: 52.549, lng: 13.422},
        {lat: 52.497, lng: 13.396},
        {lat: 52.517, lng: 13.394}
      ];
    """
    to_render = []

    pin = str(pincode)
    response = search(pin)
    all_businesses = response['businesses']

    for business in all_businesses:
        lats_lngs = {}
        lat = business['coordinates']['latitude']
        lats_lngs['lat'] = lat
        lng = business['coordinates']['longitude']
        lats_lngs['lng'] = lng
        to_render.append(lats_lngs)

    return to_render

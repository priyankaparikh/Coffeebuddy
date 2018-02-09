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


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
API_KEY= 


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'coffee'
#DEFAULT_LOCATION = 'San Francisco, CA'
DEFAULT_LOCATION = '95134'
SEARCH_LIMIT = 10


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


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)



###################################################################################

if __name__ == '__main__':
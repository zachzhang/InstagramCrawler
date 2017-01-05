from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

import requests
import BeautifulSoup
import urllib

#add ?start=90
bus_page = requests.get('https://en.yelp.be/biz_photos/mr-falafel-morgan-hill')

soup = BeautifulSoup.BeautifulSoup(bus_page.text)

img_url = 'https://s3-media1.fl.yelpcdn.com/bphoto/{}/o.jpg'

for anchor in soup.findAll('li'):

    str_anch = str(anchor)
    
    if 'data-photo-id' in str_anch:
        img_id = str_anch.split('"')[1]

        urllib.urlretrieve( img_url.format(img_id) , "./yelp_imgs/{}.jpg".format(img_id))



'''
Consumer Key	ENJtlRZ5IZ8J6Vmk0Zslpg
Consumer Secret	RNg9NDPxQ8xWHJ9a5TgedMkIKmg
Token	oy0RLL0c206ViAZnvuiJRSjeoZJB9vKN
Token Secret	vDAAJs7up04qEqyycotl8Z1QfGY

CONSUMER_KEY = 'ENJtlRZ5IZ8J6Vmk0Zslpg'
CONSUMER_SECRET = 'RNg9NDPxQ8xWHJ9a5TgedMkIKmg'
TOKEN = 'oy0RLL0c206ViAZnvuiJRSjeoZJB9vKN'
TOKEN_SECRET = 'vDAAJs7up04qEqyycotl8Z1QfGY'
'''

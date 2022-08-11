from bs4 import BeautifulSoup
import requests
from product import Product
from card import Card
import pyrebase

#----------------------------Set up---------------------------------------------
firebaseConfigs = {
    "apiKey": "AIzaSyB30g5VcxcbpEMG5nWa41X0hlciQ82J_SY",
    "authDomain": "pdp-t-9d91b.firebaseapp.com",
    "databaseURL": "https://pdp-t-9d91b-default-rtdb.firebaseio.com",
    "projectId": "pdp-t-9d91b",
    "storageBucket": "pdp-t-9d91b.appspot.com",
    "messagingSenderId": "15037414348",
    "appId": "1:15037414348:web:8140d190b619f3398d3b69",
    "measurementId": "G-G5JKZ856VF"}

firebase = pyrebase.initialize_app(firebaseConfigs)
database = firebase.database()
#-------------------------------------------------------------------------

cardsToServer = []
products = database.child('Product').get()
for product in products.each():
    if ('-D-' in product.val()['title']) and ('Ragnarok' not in product.val()['title']) and ('Touken' not in product.val()['title']):
            cards = product.val()['cards']
            for card in cards:
                if (card['rarity'] == 'RRR' or (card['rarity'] == 'SD' and int(card['grade']) >= 3)) and 'Normal Unit' in card['type'] and 'Standard' in card['regulation']:
                    print(card['name'])
                    card = Card(card['image'], card['name'], card['type'], card['nation'], card['race'], card['grade'], card['power'], card['critical'], card['shield'], card['skill'], card['effect'], card['regulation'], card['number'], card['rarity'])
                    database.child('Vanguard Ace Card').push(card.__dict__)



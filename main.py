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

htmlText = requests.get('https://en.cf-vanguard.com/cardlist/').text
soup = BeautifulSoup(htmlText, 'lxml')
productItemDivs = soup.find_all('div', class_ = 'product-item') #fix to find_all
for productItemDiv in productItemDivs:
    productImage = 'https://en.cf-vanguard.com' + productItemDiv.find('img', class_ = 'image')['src']
    productCategory = productItemDiv.find('div', class_ = 'category').text
    productTitle = productItemDiv.find('div', class_ = 'title').text
    productRelease = productItemDiv.find('div', class_ = 'release')
    if productRelease == None: 
        productRelease = None
    else: 
        productRelease = productRelease.text
    productRef = 'https://en.cf-vanguard.com' + productItemDiv.a['href']

    htmlText1 = requests.get(productRef).text
    soup1 = BeautifulSoup(htmlText1, 'lxml')
    productCards = []
    cardListDivs = soup1.find_all('div', class_ = 'cardlist_gallerylist')
    for cardList in cardListDivs:
        for index, card in enumerate(cardList.ul.findAll('li')):
            htmlText2 = requests.get('https://en.cf-vanguard.com' + card.a['href']).text
            soup2 = BeautifulSoup(htmlText2, 'lxml')
            cardInfo = soup2.find('div', class_ = 'cardlist_detail')
            cardImage = 'https://en.cf-vanguard.com' + cardInfo.find('div', class_ = 'main').img['src']
            cardName = soup2.find('span', class_ = 'face').text
            cardType = soup2.find('div', class_ = 'type').text
            cardNation = soup2.find('div', class_ = 'nation').text
            cardRace = soup2.find('div', class_ = 'race').text
            cardGrade = soup2.find('div', class_ = 'grade').text.replace('Grade ', '')
            cardPower = soup2.find('div', class_ = 'power').text.replace('Power ', '')
            cardCritical = soup2.find('div', class_ = 'critical').text.replace('Critical ', '')
            cardShield = soup2.find('div', class_ = 'shield').text.replace('Shield ', '')
            cardSkill = soup2.find('div', class_ = 'skill').text
            cardEffect = soup2.find('div', class_ = 'effect').text
            cardRegulation = soup2.find('div', class_ = 'regulation').text
            cardNumber = soup2.find('div', class_ = 'number').text
            cardRarity = soup2.find('div', class_ = 'rarity').text
            theCard = Card(cardImage, cardName, cardType, cardNation, cardRace, cardGrade, cardPower, cardCritical, cardShield, cardSkill, cardEffect, cardRegulation, cardNumber, cardRarity)
            productCards.append(theCard.__dict__)
            

    prod = Product(productImage, productCategory, productTitle, productRelease, productRef, productCards)
    database.child('Product').push(prod.__dict__)
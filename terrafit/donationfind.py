from bs4 import BeautifulSoup
import requests
from selenium import webdriver

PATH = "/Users/alliewu/Desktop/chromedriver"
driver = webdriver.Chrome(PATH)
zip = '77005'
link = 'http://google.com/maps/search/' + zip + '+donation+clothes/'
driver.get(link)
places = driver.find_elements_by_class_name('section-result-title')
centers = [f.text for f in places]
names = driver.find_elements_by_class_name('section-result-location')
addresses = [a.text for a in names]
don = {}
for i in range(len(centers)):
    don[centers[i]] = addresses[i]



from bs4 import BeautifulSoup
import requests
from selenium import webdriver

def get_places(zip):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    PATH = "/Users/alliewu/Desktop/chromedriver"
    driver = webdriver.Chrome(PATH, options=options)
    link = 'http://google.com/maps/search/' + zip + '+donation+clothes/'
    driver.get(link)
    places = driver.find_elements_by_class_name('section-result-title')
    centers = [f.text for f in places]
    names = driver.find_elements_by_class_name('section-result-location')
    addresses = [a.text for a in names]
    d = []
    for i in range(len(centers)):
        if centers[i] != '' and addresses[i] != '':
            don = {}
            don['center'] = centers[i]
            don['address'] = addresses[i]
            d.append(don)

    driver.close()
    driver.quit()
    return d







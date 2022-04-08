import shutil
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import requests
import json
import os
import time


make_url = lambda country, asin: f"https://www.amazon.{country}/dp/{asin}"
input_csv_url = "https://docs.google.com/spreadsheets/d/1BZSPhk1LDrx8ytywMHWVpCqbm8URTxTJrIRkD7PnGTM/export?format=csv"
headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5',
    }

if "err_templates" not in os.listdir():
    os.mkdir("err_templates")


class Cache:

    def __init__(self):
        self.id = 0
        self.products = []
        
        if "Products_List_Output.json" in os.listdir():
            with open("Products_List_Output.json") as f:
                self.products = json.load(f)
                self.id = len(self.products)
    
    def store(self, name, img_url, price, about, url):
        content = {
            "id" : self.id,
            "product_url" : url,
            "url" : url,
            "product_title" : name,
            "title" : name,
            "product_image_url" : img_url,
            "img_url" : img_url,
            "product_price" : price,
            "price" : price,
            "about_product" : about,
            "about" : about,
        }
        print("Storing", *content.items())
        self.products.append(content)
        self.id += 1
    
    def convert_cache_to_json(self):
        # print(self.products, self.id)
        with open("Products_List_Output.json", 'w') as f:
            # f.write(json.dumps(self.products))
            json.dump(self.products, f, indent= 4, separators= (', ', ': '))


def to_file(name, r):
    with open("./err_templates/" + name + ".html", 'w') as f:
        f.write(r.content.decode('utf-8'))

    return



def download_csv_urls_into_file():
    df = pd.read_csv(input_csv_url)

    countries = list()
    asins = list()
    pre_urls = dict()

    # To check all columns list use df.columns

    for i, j in zip(df.country, df.Asin):
        countries.append(i)
        asins.append(j)
        pre_urls[(i,j)] = make_url(i, j)

    content = dict()
    content['countries'] = countries
    content['asins'] = asins
    content['pre_urls'] = pre_urls

    with open("Amazon Urls Input.pkl", "wb") as f:
        pickle.dump(content, f)

    return None



def load_urls_from_file():
    try:
        with open("Amazon Urls Input.pkl", "rb") as f:
            content = pickle.load(f)
        
        countries = content.get("countries")
        asins = content.get("asins")
        pre_urls = content.get("pre_urls")

        return countries, asins, pre_urls
    except Exception as e:
        print(e)
    
    return (None, None, None)


def load_urls_from_csv_url():
    df = pd.read_csv(input_csv_url)

    countries = df.country
    asins = df.Asin
    pre_urls = dict(((i,j), make_url(i, j)) for i, j in zip(df.country, df.Asin))

    return (countries, asins, pre_urls)



def extract(r, obj):
    soup = BeautifulSoup(r.content, "html5lib")
    product_name, product_img_url, product_price, about_product  =  None, None, None, None

    try:
        element1 = (    soup.find("img", attrs= {'id' : "landingImage"}) 
                    or soup.find("img", attrs= {'id' : "igImage"}) 
                    or soup.find("img", attrs= {'id' : "imgBlkFront"}) 
                    or {})
        product_img_url = element1.get("src")

    except AttributeError:
        print("Image URL Tag error,", r.url)

    try:
        title = (      soup.find("span", attrs={"id": 'productTitle'}) 
                    # or soup.find("span", attrs={"id": 'productTitle'}) 
                    or None)
        subtitle = (   soup.find("span", attrs={"id": 'productSubtitle'}) 
                    or None)
        product_name = title.get_text("\n", strip= True) + subtitle.get_text("\n", strip= True)

    except AttributeError:
        print("Title/Subtitle Tag error,", r.url)

    try:
        element2 = (    soup.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}) 
                    or soup.find('div', attrs = {'id':'tmmSwatches'}) 
                    or soup.find('span', attrs = {'class':'a-color-price'}) 
                    or soup.find('span', attrs = {'class':'a-color-base'}) 
                    or None)
        product_price = element2.get_text("\n", strip= True)
    
    except AttributeError:
        print("Price Tag error,", r.url)

    try:
        element3 = (    soup.find("div", attrs= {'id' : 'feature-bullets'}) 
                    or soup.find("div", attrs= {'class' : "a-expander-content a-expander-partial-collapse-content"})
                    or soup.find("div", attrs= {'id' : 'detailBullets_feature_div'})
                    or None)
        about_product = element3.get_text("\n", strip= True)
    
    except AttributeError:
        print("About Tag error,", r.url)

    return product_name, product_img_url, product_price, about_product


def visit_url(obj, url):
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5',
    }

    with requests.Session() as s:
        r = s.get(url, headers= headers)
        

    if r.status_code == 200:                                        # Status OK
        # to_file(str(obj.id) + '200', r)
        obj.store(*extract(r, obj), url)

    # elif r.status_code == 503:                                      # Status Unauthorized, Captcha is needed to be filled
    #     # to_file(str(obj.id) + '503', r)
    #     get_captcha(r)
    #     print(resolve_captcha("./captcha.jpg"))

    elif r.status_code == 404:                                      # Page not found
        # to_file(str(obj.id) + '404', r)
        print(f"Webpage not found, {url} not available")
    
    else:
        to_file(str(obj.id) + str(r.status_code), r)
        print("Unknown Error with status code=", r.status_code)

    return


if __name__ == "__main__":
    # download_csv_urls_into_file()
    # countries, asins, pre_urls = load_urls_from_file()
    
    countries, asins, pre_urls = load_urls_from_csv_url()
    obj = Cache()
    
    for i in range(1000):    
        country, asin = countries[i], asins[i]

        url = make_url(country, asin)
        # print(url)


        visit_url(obj, url)


    obj.convert_cache_to_json()
    # exit()

# Stowaway Codes for debugging

url = "https://www.amazon.fr/dp/000103863X"
with requests.Session() as s:
  r = s.get(url, headers= headers)
  soup = BeautifulSoup(r.content, "html5lib")


a = soup.find("div", attrs= {'id' : "tmmSwatches"})
"a-expander-content a-expander-partial-collapse-content"
# for span in a.find_all("span"):
#   print(span.text)

a.get_text("\n", True)

# For clearing out unnecessary files
# shutil.rmtree('err_templates')

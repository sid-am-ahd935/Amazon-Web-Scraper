#### **Importing Libraries**

from bs4 import BeautifulSoup
import pandas as pd
import pickle
import requests
import json
import os
import time

#### **Small Snippets for collecting data used in between.**


make_url = lambda country, asin: f"https://www.amazon.{country}/dp/{asin}"
input_csv_url = "https://docs.google.com/spreadsheets/d/1BZSPhk1LDrx8ytywMHWVpCqbm8URTxTJrIRkD7PnGTM/export?format=csv"
headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5',
    }

num_prefix = {
    11 : '11th',
    12 : '12th',
    13 : '13th',
    1 : '1st',
    2 : '2nd',
    3 : '3rd',
}

if "err_templates" not in os.listdir():
    os.mkdir("err_templates")


#### **A custom class to store the scraped data in cache which is then stored as a JSON file. Additionally, it all stores the time stamps of each round.**

class Cache:

    def __init__(self):
        self.id = 0
        self.products = []
        self.time_stamps = []
        
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
        
        with open("Time_Stamps_List_Output.json", 'w') as f:
            json.dump(self.time_stamps, f, indent= 4, separators= (', ', ': '))
    
    def mark_time(self, t1, t2, n, div):
      t = t2 - t1
      content = f"Time taken for {num_prefix.get(n, str(n)+'th')} round of {div} visits:  {t} seconds"
      self.time_stamps.append(content)



def to_file(name, r):
    with open("./err_templates/" + name + ".html", 'w') as f:
        f.write(r.content.decode('utf-8'))

    return


#### ***For slow/unstable network connections, it is advisable to download the given csv file and load the feeding data from there***


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


#### ***For normal purposes, load the feeding data directly from the csv document given in the url.***

def load_urls_from_csv_url():
    df = pd.read_csv(input_csv_url)

    countries = df.country
    asins = df.Asin
    pre_urls = dict(((i,j), make_url(i, j)) for i, j in zip(df.country, df.Asin))

    return (countries, asins, pre_urls)



#### ***This function that extracts data from the given HTML content and then stores the extracted data into the cache.***

def extract(r, obj):
    soup = BeautifulSoup(r.content, "html5lib")
    product_name, product_img_url, product_price, about_product  =  None, None, None, None

    try:
        element1 = (    soup.find("img", attrs= {'id' : "landingImage"}) 
                    or soup.find("img", attrs= {'id' : "igImage"}) 
                    or soup.find("img", attrs= {'id' : "imgBlkFront"}) 
                    or None)
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


#### ***The function that takes in the url to visit, visits it, then according the visiting status, either gives the response object to the extractor function or handles other responses accordingly.***

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
        to_file(str(r.status_code) + str(r.url.rsplit("/", 1)[1]), r)
        print("Unknown Error with status code=", r.status_code)

    return r


#### ***The main function of this program file, runs by itself only when this program is ran specifically and this function carries out the main logic: Loading all input urls, Visiting each one by one, storing in the cache, then at the end of the program creating the a JSON file to store the data.***



def main():
    # download_csv_urls_into_file()
    # countries, asins, pre_urls = load_urls_from_file()
    
    countries, asins, pre_urls = load_urls_from_csv_url()
    obj = Cache()
    
    t1 = time.time()
    div = 10                           # Division Of Each Round
    seconds_to_sleep = 0               # Each time sleep increases to escape bot catcher
    max_sleep_allowed = 60             # Max sleep allowed
    i = 0

    while i < 1000:   
        country, asin = countries[i], asins[i]

        url = make_url(country, asin)
        # print(url)


        r = visit_url(obj, url)

        if r.status_code == 503:
            print("Standing by... Our bot has been detected...")
            i -= 1
            seconds_to_sleep += 10
            if seconds_to_sleep >= max_sleep_allowed:        # Max sleep reached
                print("Solve the captcha to further continue the process: ", url)
                break
            else:
                time.sleep(seconds_to_sleep)

        if i % div == 0:
            t2 = time.time()
            obj.mark_time(t1, t2, i//div, div)
            t1 = t2
            time.sleep(div)
        
        i += 1




    obj.convert_cache_to_json()

    return


if __name__ == "__main__":
    main()
    # exit()

##### ***These snippets are used for debugging and clearing out unnecessary files for cleaning up.***

# Stowaway Codes for debugging
def extract_by_url_and_returning_data_for_debugging_purposes_by_tweaking_the_function_itself():
    url = "https://www.amazon.fr/dp/000103863X"
    with requests.Session() as s:
      r = s.get(url, headers= headers)
      soup = BeautifulSoup(r.content, "html5lib")


    a = soup.find("div", attrs= {'id' : "tmmSwatches"})
    "a-expander-content a-expander-partial-collapse-content"
    # for span in a.find_all("span"):
    #   print(span.text)
    return r.url.rsplit("/", 1)[1], r.status_code
    return a.get_text("\n", True)

# extract_by_url_and_returning_data_for_debugging_purposes_by_tweaking_the_function_itself()

# For clearing out unnecessary files
def cleanup():
    ch = input("Do you want to clean the collected error HTML templates files: [Y/n] ")
    if not (ch == 'n'):
        import shutil
        try:  shutil.rmtree('err_templates')
        except FileNotFoundError: pass


    ch = input("Do you want to remove the Time Stamp file: [Y/n] ")
    if not (ch == 'n'):
        try:  os.remove("Time_Stamps_List_Output.json")
        except FileNotFoundError: pass

    ch = input("Do you want to remove the JSON file: [y/N] ")
    if (ch == 'y'):
        try:  os.remove('Products_List_Output.json')
        except FileNotFoundError: pass


# cleanup()
    

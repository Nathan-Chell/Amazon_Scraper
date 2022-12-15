#Scrape amazon to collect data about the top 10 results for a given item.

import pandas as pd
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup



def getData(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)
    try:
        product = {
            'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
            'price': r.html.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[1]', first=True).text,
            'rating': r.html.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span', first=True).text,
            'total_reviews': r.html.xpath('//*[@id="acrCustomerReviewText"]', first=True).text,
            'availability': r.html.xpath('//*[@id="availability"]', first=True).text,
            'about': r.html.xpath('//*[@id="feature-bullets"]/ul', first=True).text.split("})")[1],
            'image' : r.html.xpath('/html/body/div[2]/div[2]/div[6]/div[5]/div[3]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[1]/span/span/div/img', first=True),
            'url' : ''
        }
    except:
        try:
            product = {
                'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
                'price': r.html.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[1]', first=True).text,
                'rating': r.html.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span', first=True).text,
                'total_reviews': r.html.xpath('//*[@id="acrCustomerReviewText"]', first=True).text,
                'availability': r.html.xpath('//*[@id="availability"]', first=True).text,
                'about': r.html.xpath('//*[@id="feature-bullets"]/ul', first=True).text.split("})")[1],
                'image': r.html.xpath('/html/body/div[2]/div[2]/div[6]/div[5]/div[3]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[1]/span/span/div/img', first=True),
                'url' : ''
            }
        except:
            print("Error finding a detail")
            product = {}

    return product


def main():

    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

    item = "fridge"
    URL = ("https://www.amazon.co.uk/s?k={}&ref=nb_sb_noss".format(item))

    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "lxml")
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    urls = []

    for i, link in enumerate(links):
        if i < 1:
            urls.append(link.get('href'))

    data = []
    for url in urls:
        product_details = getData("https://amazon.co.uk" + url)
        product_details['image'] = str(product_details['image']).split("data-a-dynamic-image='{")[1].split(":[")[0].replace('"','')
        product_details['url'] = ("https://amazon.co.uk" + url)
        data.append(product_details)

    for i in range(len(data)):
        print(data[i])



if __name__ == '__main__':
    main()


#'https://www.amazon.co.uk/Hisense-RR220D4ADF-128x52cm-Freestanding-Fridge/dp/B08NF8RTWW/ref=sr_1_1_sspa?crid=2KIZVNPXF750D&keywords=fridge&qid=1671138738&sprefix=%2Caps%2C115&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1',
#        'https://www.amazon.co.uk/Undercounter-Larder-Fridge-Freestanding-Capacity/dp/B0B5X2LMGZ/ref=sr_1_2_sspa?crid=2KIZVNPXF750D&keywords=fridge&qid=1671138920&sprefix=%2Caps%2C115&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1&smid=A23JPYTMWHPQTN',
#        'https://www.amazon.co.uk/COMFEE-Fridge-RCD132WH1-Counter-Reversible/dp/B08Q8ZN4S3/ref=sr_1_3?crid=2KIZVNPXF750D&keywords=fridge&qid=1671138920&sprefix=%2Caps%2C115&sr=8-3&th=1']

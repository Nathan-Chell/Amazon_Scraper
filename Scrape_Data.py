#Scrape amazon to collect data about the top 10 results for a given item.

import bs4
from requests_html import HTMLSession
import pandas as pd



def getPrice(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)
    try:
        product = {
            'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
            'price': r.html.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[1]', first=True).text
        }
    except:
        try:
            product = {
                'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
                'price': r.html.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[1]', first=True).text
            }
        except:
            print("Error finding a detail")

    return product


def main():


    urls = ['https://www.amazon.co.uk/Hisense-RR220D4ADF-128x52cm-Freestanding-Fridge/dp/B08NF8RTWW/ref=sr_1_1_sspa?crid=2KIZVNPXF750D&keywords=fridge&qid=1671138738&sprefix=%2Caps%2C115&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1',
            'https://www.amazon.co.uk/Undercounter-Larder-Fridge-Freestanding-Capacity/dp/B0B5X2LMGZ/ref=sr_1_2_sspa?crid=2KIZVNPXF750D&keywords=fridge&qid=1671138920&sprefix=%2Caps%2C115&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1&smid=A23JPYTMWHPQTN',
            'https://www.amazon.co.uk/COMFEE-Fridge-RCD132WH1-Counter-Reversible/dp/B08Q8ZN4S3/ref=sr_1_3?crid=2KIZVNPXF750D&keywords=fridge&qid=1671138920&sprefix=%2Caps%2C115&sr=8-3&th=1']

    data = []
    for url in urls:
        data.append(getPrice(url))

    print(data)

if __name__ == '__main__':
    main()

#Scrape amazon to collect data about the top 10 results for a given item.

from bs4 import BeautifulSoup
import requests


def get_title(soup):

    try:
        #Outer tag
        title = soup.find("span", attrs={"id":'productTitle'})

        #INner tag
        title_string = title.string.strip()

    except AttributeError:
        title_string = ""

    return title_string

def get_price(soup):
    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'class':'a-price'}).string.strip()
        except:
            price = ""

    return price

def get_rating(soup):
    try:
        rating = soup.find('span', attrs={'class':'a-size-base'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("i", attrs={'class', 'a-icon a-icon-star a-star-4-5'}).string.strip()
        except:
            rating = ""
    return rating

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'class':'a-size-base s-underline-text'}).string.strip()
    except AttributeError:
        try:
            review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
        except AttributeError:
            review_count = ""
    return review_count

def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        try:
            available = soup.find("span", attrs={'span':'a-size-base a-color-price'}).string.strip()
        except:
            available = "Unknown"

    return available

def main():

    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US'})

    URL = 'https://www.amazon.com/s?k=fridge&ref=nb_sb_noss'

    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "lxml")

    links = soup.find_all('a', attrs={'class': 'a-link-normal s-no-outline'})

    links_list = []

    for i, link in enumerate(links):
        if i < 7:
            links_list.append(link.get('href'))

    for link in links_list:

        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "lxml")

        print("Title = {}".format(get_title(new_soup)))
        print("Price = {}".format(get_price(new_soup)))
        print("Rating = {}".format(get_rating(new_soup)))
        print("reviews = {}".format(get_review_count(new_soup)))
        print("availability = {}".format(get_availability(new_soup)))
        print()

if __name__ == '__main__':
    main()

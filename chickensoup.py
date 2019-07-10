#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
import requests
import csv
import sys

def get_links(url="https://www.skroutz.gr/c/40/kinhta-thlefwna.html?from=families&page=2"):
    res = requests.get(url)
    souped = bs(res.text, "html.parser")
    for match in souped.find_all("span"):
        match.extract()
    list_with_phones = souped.find_all(
        class_="js-sku-link image_link")  # Hacky
    '''Write to CSV later'''
    names, prices = [phone.get('title') for phone in list_with_phones], [
        price.text.strip() for price in souped.find_all(class_="price react-component")]

    # for name, price in zip(names, prices):
    #    print("{0} -> {1}".format(name, price))
    return zip(names, prices)


def write_to_csv(data, path):
    try:
        out = csv.writer(open(path, 'w'))
        out.writerow(['Name', 'Price'])
        for row in data:
            for name, price in row:
                out.writerow([name, price])
    except IOError as er:
        raise er
    finally:
        print("Written to file")


if __name__ == "__main__":

    x = []
    for i in range(1, int(sys.argv[1])):
        x.append(get_links(
            "https://www.skroutz.gr/c/40/kinhta-thlefwna.html?from=families&page={0}".format(int(i))))
    write_to_csv(x, "data.csv") 

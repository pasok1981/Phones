#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
import requests
import csv
import sys
import time
import getopt

def get_links(url):
    res = requests.get(url)
    souped = bs(res.text, "html.parser")
    for match in souped.find_all("span"):
        match.extract()
    names, prices = [phone.get('title') for phone in souped.find_all(
        class_="js-sku-link image_link")], [
        price.text.strip() for price in souped.find_all(class_="price react-component")]

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
        print("Attempted to write data to file {}".format(path))


def main():
    start, end=0, 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'se:h', ['help', 'start=', 'end='])
    except getopt.GetoptError as er:
        print(str(er))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print("chickensoup.py --start=<start page> --end=<last page>")
            sys.exit()
        elif opt == '--start':
            start = int(arg)
        elif opt == '--end':
            end = int(arg)
        else:
            assert False, "Unsupported option"
            
    print("Starting from: {}".format(start))
    print("End: {}".format(end))

    x = []
    for i in range(start, end):
        x.append(get_links(
            "https://www.skroutz.gr/c/40/kinhta-thlefwna.html?from=families&page={0}".format(int(i))))

        if i % 10 == 0:
            time.sleep(5)
            print ("Going to Sleep...")

    write_to_csv(x, "data.csv")

if __name__ == "__main__":
    main()

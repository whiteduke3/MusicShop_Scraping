from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import os
import csv
import json

if os.path.exists("C:\\Users\\Home\\PycharmProjects\\musicmaxx_scraping\\cijene.csv"):
    os.remove("C:\\Users\\Home\\PycharmProjects\\musicmaxx_scraping\\cijene.csv")

if os.path.exists(r'Prices.json'):
    os.remove(r'Prices.json')

url = "https://musicmax.si/c11545sl/c11546sl/"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}


request = Request(url,None,headers)
page_request = urlopen(request)
soupy = bs(page_request, "html.parser")
pagination = soupy.find_all("ul", "pagination")[0]
pagenum_to_search = len(pagination.find_all("li")) - 2

url_links = ["https://musicmax.si/c11545sl/c11546sl/"] + \
            ["https://musicmax.si/c11545sl/c11546sl/?page=" + str(i) for i in range(2, pagenum_to_search + 1)]

with open("cijene.csv", mode="w", encoding="utf-8") as f:
    file_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow((["IME_GITARE", "NEW_PRICE(EUR)", "OLD_PRICE(EUR)"]))
    for url in url_links:
        request1 = Request(url,None,headers)
        page_url = urlopen(request1)
        soup = bs(page_url, "html.parser")
        for thumb in soup.find_all("div", "product-thumb"):
            for caption in thumb.find_all("div", "caption"):
                ime_gitare = caption.h4.a.string
                prices = caption.find_all("p", "price")[0]
                price_new = prices.span.string
                price_old = prices.find_all("span", "price-old")[0].string
                file_writer.writerow(([ime_gitare, price_new[:-1], price_old[:-1]]))


def make_json(csvFilePath, jsonFilePath):
    data = {}
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for i,rows in enumerate(csvReader):
            key = rows['IME_GITARE']
            data['GUITAR'+str(i)] = rows

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, ensure_ascii=False,indent=4))


csvFilePath = r'cijene.csv'
jsonFilePath = r'Prices.json'

make_json(csvFilePath, jsonFilePath)

print("CSV and JSON files created successfully")

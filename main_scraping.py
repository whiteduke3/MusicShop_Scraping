from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import os
import csv

if os.path.exists("C:\\Users\\Home\\PycharmProjects\\musicmaxx_scraping\\cijene.csv"):
    os.remove("C:\\Users\\Home\\PycharmProjects\\musicmaxx_scraping\\cijene.csv")

page_request = urlopen("https://musicmax.si/c11545sl/c11546sl/")
soupy = bs(page_request, "html.parser")
pagination = soupy.find_all("ul", "pagination")[0]
pagenum_to_search = len(pagination.find_all("li")) - 2

url_links = ["https://musicmax.si/c11545sl/c11546sl/"] + \
            ["https://musicmax.si/c11545sl/c11546sl/?page=" + str(i) for i in range(2, pagenum_to_search + 1)]

with open("cijene.csv", mode="w", encoding="utf-8") as f:
    file_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow((["IME_GITARE", "N_CIJENA(euro)", "S_CIJENA(euro)"]))
    for url in url_links:
        page_url = urlopen(url)
        soup = bs(page_url, "html.parser")
        for thumb in soup.find_all("div", "product-thumb"):
            for caption in thumb.find_all("div", "caption"):
                ime_gitare = caption.h4.a.string
                prices = caption.find_all("p", "price")[0]
                price_new = prices.span.string
                price_old = prices.find_all("span", "price-old")[0].string
                file_writer.writerow(([ime_gitare, price_new[:-1], price_old[:-1]]))

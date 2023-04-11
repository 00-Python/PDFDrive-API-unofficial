# scrapper for pdfdive.net

import requests
from bs4 import BeautifulSoup
import wget
import os
import re

BASEURL = "http://www.pdfdrive.com"


# get collections from homepage
def get_collections_info():
    collections = []
    r = requests.get(BASEURL)
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.find_all("div", class_="collection-title mb-2"):
        # get text
        text = a.text
        # remove \n
        text = text.replace("\n", "")
        if text[0] == " ":
            text = text[1:]
        # get link
        link = a.find("a")["href"]

        # make dict
        collection = {
            "name": text,
            "link": link
        }

        # append to collections
        collections.append(collection)
    return collections


def get_collections_books():
    collections = get_collections_info()
    for collection in collections:
        # get books
        books = []
        r = requests.get(BASEURL + collection["link"])
        soup = BeautifulSoup(r.text, "html.parser")
        # get files-new div
        files_new = soup.find("div", class_="files-new")
        rows = files_new.find_all("div", class_="row")
        book_amount = len(rows)
        data = []
        for row in rows:
            # get title from h2 tag
            title = row.find("h2").text
            # if the first character is a space, remove it
            if title[0] == " ":
                title = title[1:]
            # get link from href
            link = row.find("a")["href"]

            # TODO - get the rest of the data i.e. author, description, downloads, image link, etc.

            # append to data
            data.append({
                "title": title,
                "link": link
            })
        # add quantity of books per category
        collection["quantity"] = book_amount
        # add books to collection
        collection["books"] = data
    return collections


def get_download_link(link):
    r = requests.get(BASEURL + link)
    soup = BeautifulSoup(r.text, "html.parser")
    # get middle link from element with id download-button-link
    mid_link = soup.find("a", id="download-button-link")["href"]

    # TODO - add a way to load up the page with the middle link and get the download link from there (selenium?)
    
    r = requests.get(BASEURL + mid_link)
    soup = BeautifulSoup(r.text, "html.parser")
    # get download link from href
    return soup


def download_book(link):
    download_link = BASEURL + get_download_link(link)
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    # download file into downloads folder
    wget.download(download_link, out="downloads/")


def search(book):
    pass


if __name__ == "__main__":
    collections = get_collections_books()
    print(len(collections))
    book_link = collections[0]["books"][0]["link"]
    book_title = collections[0]["books"][0]["title"]
    print(book_link, "\n" + book_title)
    print(book_title[0])
    # download_book(book_link)
    print(get_download_link(book_link))
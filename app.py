from selenium import webdriver
import pickle
import os
import time

from getlistings import getListings
from sendemail import sendEmail


if __name__ == "__main__":
    SAVED_DATA = "listing.data"
    EMAIL_SUBJECT = "New Grailed.com listing"
    with open("searches.txt") as f:
        searches = f.read().splitlines()
    searches = [search for search in searches if search != ""]

    if os.path.isfile(SAVED_DATA):
        os.remove(SAVED_DATA)

    count = 0
    driver = webdriver.Firefox()
    while(count < 20):
        # create listing data
        listing_data = []
        for search_url in searches:
            listing_data.append(getListings(driver, search_url))

        # check current listings against old listings
        if os.path.isfile(SAVED_DATA):
            with open(SAVED_DATA, "rb") as filehandle:
                old_listings = pickle.load(filehandle)
                for i in range(len(searches)):
                    for listing in listing_data[i]:
                        if listing not in old_listings[i]:
                            count += 1
                            print(listing)
                            sendEmail(EMAIL_SUBJECT, listing)

        # save listings to file
        with open(SAVED_DATA, "wb") as filehandle:
            pickle.dump(listing_data, filehandle)


        time.sleep(10 * 60)
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
    listings = {}
    for search in searches:
        if search != "":
            listings[search] = None

    driver = webdriver.Firefox()
    count = 0
    while(count < 20):

        next_listings = {}
        for search, old_results in listings.items():
            new_results = getListings(driver, search)

            # check for new listings if old results exist
            if old_results != None:
                for result in new_results:
                    if result not in old_results:
                        count += 1
                        print(result)
                        sendEmail(EMAIL_SUBJECT, result)
            else:
                old_results = []

            if new_results:
                next_listings[search] = new_results
            else: # avoid feeding nothing when getListings incorrectly returns nothing
                next_listings[search] = old_results

        listings = next_listings

        time.sleep(5 * 60)


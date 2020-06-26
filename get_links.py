# selenium stup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# to find links
from bs4 import BeautifulSoup
import json
import urllib.request
import re

import time # to sleep

# fill this in with your job preferences!
PREFERENCES = {
    "position_title": "",
    "location": "  ",
    "username": "",
    "password": ""
}

def login(driver):
    #login to glassdoor
    driver.get('https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK')
    driver.maximize_window()
    
    username_field = driver.find_element_by_xpath("//*[@id='userEmail']")
    password_field = driver.find_element_by_xpath("//*[@id='userPassword']")
    
    username_field.clear()
    password_field.clear()
    
    username_field.send_keys(PREFERENCES['username'])
    password_field.send_keys(PREFERENCES['password'])
    
    driver.find_element_by_xpath("//*[@id='InlineLoginModule']/div/div/div/div/div[3]/form/div[3]/div[1]").click()
    
    return True

# navigate to appropriate job listing page
def go_to_listings(driver):

    # wait for the search bar to appear
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='scBar']"))
        )

    try:
        # look for search bar fields
        position_field = driver.find_element_by_xpath("//*[@id='sc.keyword']")
        location_field = driver.find_element_by_xpath("//*[@id='sc.location']")
        location_field.clear()

        # fill in with pre-defined data
        position_field.send_keys(PREFERENCES['position_title'])
        location_field.clear()
        location_field.send_keys(PREFERENCES['location'])

        # wait for a little so location gets set
        time.sleep(1)
        driver.find_element_by_xpath(" //*[@id='scBar']/div/button").click()

        # close a random popup if it shows up
        try:
            driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
        except NoSuchElementException:
            pass
        
        time.sleep(3)
        
        
        try:
            driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
        except NoSuchElementException:
            pass
        
        #Adding Filters to the search results
        try:
            
            remote = "//*[@id='dynamicFiltersContainer']/div/div[1]/div[2]/div[2]/div[15]/label"

            more_menu = driver.find_element_by_xpath("//*[@id='dynamicFiltersContainer']/div/div[1]/div[2]")
            more_menu.click()
            time.sleep(.5)
            
            driver.find_element_by_xpath(remote).click()
            
            time.sleep(1)
            easy_apply = driver.find_element_by_xpath("//*[@id='dynamicFiltersContainer']/div/div[1]/div[2]/div[2]/div[14]/label/div")
            easy_apply.click()
            
            time.sleep(1)
            
            driver.find_element_by_xpath(remote).click()
        
        
            element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='MainCol']/div[1]/ul"))
                )
            
            time.sleep(2)
        

            more_menu.click()
            
            
            #Intern
            driver.find_element_by_xpath("//*[@id='filter_jobType']").click()
            time.sleep(.3)
            driver.find_element_by_xpath("//*[@id='PrimaryDropdown']/ul/li[5]/span[1]").click()
            
            time.sleep(.5)
            
        except NoSuchElementException:
            pass
        
        #driver.minimize_window()
        
        return True

    # note: please ignore all crappy error handling haha
    except NoSuchElementException:
        return False

# aggregate all url links in a set
def aggregate_links(driver):
    allLinks = [] # all hrefs that exist on the page

    # wait for page to fully load
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='MainCol']/div[1]/ul"))
        )

    


    # parse the page source using beautiful soup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source)

    # find all hrefs
    allJobLinks = soup.findAll("a", {"class": "jobLink"})
    allLinks = [jobLink['href'] for jobLink in allJobLinks]
    allLinks = list(dict.fromkeys(list(allLinks)))
    
    allFixedLinks = []

    # clean up the job links by opening, modifying, and 'unraveling' the URL
    for link in allLinks:
        # first, replace GD_JOB_AD with GD_JOB_VIEW
        link = link.replace("GD_JOB_AD", "GD_JOB_VIEW")

        # if there is no glassdoor prefex, add that
        # for example, /partner/jobListing.htm?pos=121... needs the prefix

        if link[0] == '/':
            link = f"https://www.glassdoor.com{link}"
            
            
        #for glassdoor links no redirect happens
        newLink = link
        allFixedLinks.append(newLink)
 
    # convert to a set to eliminate duplicates
    return set(allFixedLinks)

# 'main' method to iterate through all pages and aggregate URLs
def getURLs():
    driver = webdriver.Chrome(executable_path='/home/picklesueat/Downloads/chromedriver_linux64/chromedriver')
    success = login(driver)
    if not success:
        # close the page if it gets stuck at some point - this logic can be improved
        driver.close()

    success = go_to_listings(driver)
    if not success:
        driver.close()

    allLinks = set()
    page = 1
    next_url = ''
    while page < 2: # pick an arbitrary number of pages so this doesn't run infinitely
        print(f'\nNEXT PAGE #: {page}\n')

        # on the first page, the URL is unique and doesn't have a field for the page number
        if page < 4:
            # aggregate links on first page
            allLinks.update(aggregate_links(driver))
            
            driver.find_element_by_xpath("//*[@id='FooterPageNav']/div/ul/li["+str(page + 2)+"]").click()
            
            
            
            
            time.sleep(.75)
            try:
                driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
            except Exception:
                pass

            page += 1 

        # same patterns from page 3 onwards
        if page > 3 :
            allLinks.update(aggregate_links(driver))
            driver.find_element_by_xpath("//*[@id='FooterPageNav']/div/ul/li[5]").click()
            
            
            time.sleep(.75)
            try:
                driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
            except Exception:
                pass

            page += 1 

    driver.close()
    print(len(allLinks))
    return allLinks

# for testing purpose
#getURLs()
    


import pathlib
import time
import math
import sys
import json

from datetime import datetime
from datetime import date
from datetime import timedelta
from selenium import webdriver
from Logging import Logging
from Extract import Extract
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from HandleProperties import HandleProperties
from oslo_concurrency import lockutils
import pandas as pd

scraping_script_path   = pathlib.Path(__file__).parents[0]


class ScrapeWebsite:
    # Initialization Function
    def __init__(self, prv, city, proc_name):
        # properties needed
        # Fetching Configuration From Properties File
        self.data = {}
        self.logger                 = Logging().get_logger("scraping-log-" + prv + city + proc_name)
        self.scraping_script_path   = pathlib.Path(__file__).parents[1]
        self.handleProperties       = HandleProperties()
        self.configuration          = self.handleProperties.read_properties(
                                            str(self.scraping_script_path) + "/src/config/Scraping.properties"
                                        )
        # Initializing Data From Properties file to Execute Web Scraping
        self.file_path              = str(self.scraping_script_path) + "/src/Location.json"
        self.driver                 = str(self.scraping_script_path) + "/src/driver/chromedriver96"
        print(self.driver)


    # Function to get paramters set by the user for scrapping
    def getParameters(self, argv):
        # Get System Parameters
        total_command_line_arguments = len(argv)
        print("Length of Arguments : " + str(total_command_line_arguments))
        self.logger.debug("Length of Arguments : " + str(total_command_line_arguments))
        if total_command_line_arguments < 3:
            print("Scraping Module : Incorrect No Of Arguments Passed")
            print("Scraping Module : System exiting")
            sys.exit("Scraping Module : Incorrect No Of Arguments Passed")
        else:
            province_argument = argv[0]
            city_argument = argv[1]
            search_keywords = argv[3]
            type_argument = "w"
            

        return province_argument, city_argument, type_argument, search_keywords


    # Multiple Process Safety Configuration
    # Opening File with UTF-8 Encoding
    # Both READ-MODE and WRITE-MODE handled using this Method
    @lockutils.synchronized('not_thread_process_safe', external=True, fair=True, lock_path=str(scraping_script_path) + "/Lock/")
    def openFile(self, openMode, location_dictionary):
        # Function to help load or dump json objects
        if openMode == "r":
            with open(self.file_path, openMode, encoding="utf-8") as jsonFile:
                return json.load(jsonFile)
        if openMode == "w":
            with open(self.file_path, openMode, encoding="utf-8") as jsonFile:
                json.dump(location_dictionary, jsonFile)

            jsonFile.close()


    # This Method is used to Extract Specific Link from Anchor Tag Selenium Elements
    def extract_link(self, data_event, link_type):
        attribute_selected_elements = self.browser.find_elements_by_tag_name("a")
        if link_type == "Real Estate " or link_type == "Wanted " or link_type == "Offering ":
            for selected_elements in attribute_selected_elements:
                if selected_elements.get_attribute('data-event') == data_event and link_type == selected_elements.text.split('(')[0]:
                    link = selected_elements.get_attribute('href')
                    return link
            return ''
        elif link_type == "For Rent" or link_type == "Commercial & Other":
            for selected_elements in attribute_selected_elements:
                if selected_elements.find_elements_by_class_name("textContainer-4227985904") and selected_elements.find_elements_by_class_name("textContainer-4227985904")[0].find_element_by_tag_name('div').text == link_type:
                    link = selected_elements.get_attribute('href')
                    return link
            return ''


    def click_link(self,  link_type):
        cur_url = self.browser.current_url
        cur_url = cur_url + "&ad=" + link_type.lower()
        return cur_url
       

    # Method for Initializing Variables for Processing Location Wise Data
    def getLocationVariables(self, province_argument, city_argument, type_argument):
        # Initializing Variables for Processing Location Wise Data
        location_dictionary = self.openFile("r", "")
        province_dictionary = location_dictionary["province_dict"]
        city_dictionary = location_dictionary["city_dict"]
        province_name = province_dictionary.get(province_argument)
        cities_json = city_dictionary.get(province_argument)
        city_json = cities_json.get(city_argument)
        city_name = city_json.get("name")
        print(type_argument)

        # Checking Type of Advertisement
        if type_argument == "w":
            search_type = "Wanted"
            wanted_json = city_json.get("wanted")
            date_in_property = wanted_json["searchDate"]
            finalTimestamp_in_property = wanted_json.get("finalTimestamp")
        elif type_argument == "o":
            search_type = "Offering"
            offering_json = city_json.get("offering")
            date_in_property = offering_json["searchDate"]
            finalTimestamp_in_property = offering_json.get("finalTimestamp")


        self.logger.debug("Province is : " + str(province_dictionary))
        self.logger.info("Province Name is : " + str(province_name))
        self.logger.debug("City is : " + str(city_json))
        self.logger.debug("Cities are : " + str(cities_json))
        self.logger.info("City Name is : " + str(city_name))
        self.logger.info("Date from which Search Will Start : " + date_in_property)
        self.logger.info("Timestamp from which Search Will Start : " + finalTimestamp_in_property)
        print("Province Name is : " + str(province_name))
        # print("City is : " + str(city_json))
        # print("Cities are : " + str(cities_json))
        print("City Name is : " + str(city_name))
        print("Date from which Search Will Start : " + date_in_property)
        print("Timestamp from which Search Will Start : " + finalTimestamp_in_property)
        setValues = [type_argument, city_argument, province_argument, cities_json, province_dictionary, city_dictionary, location_dictionary, wanted_json, city_json]

        return search_type, date_in_property, finalTimestamp_in_property, province_name, city_name, setValues


    # Method to set the location to be searched
    def setLocationVariables(self, type_argument, city_argument, province_argument, cities_json, province_dictionary, city_dictionary, location_dictionary, wanted_json, city_json, current_timestamp, updated_date):
        if type_argument == "w":
            wanted_json["searchDate"] = str(updated_date)
            wanted_json["finalTimestamp"] = str(current_timestamp)
            city_json["wanted"] = wanted_json
        elif type_argument == "o":
            offering_json["searchDate"] = str(updated_date)
            offering_json["finalTimestamp"] = str(current_timestamp)
            city_json["offering"] = offering_json

        cities_json[city_argument] = city_json
        city_dictionary[province_argument] = cities_json
        location_dictionary["province_dict"] = province_dictionary
        location_dictionary["city_dict"] = city_dictionary

        return location_dictionary


    # Method for Initializing Chrome Web Driver and its Configuration
    def initBrowser(self):
        # Getting Site Url from Property Configuration
        self.site_url = self.configuration.get("url").data
        print(self.site_url)
        self.logger.debug("Scraping Module : Initiating Scraping for : " + str(self.site_url))
        print("Scraping Module : Initiating Scraping for : " + str(self.site_url))

        # Initializing Chrome Web Driver and its Configuration
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")

        try:
            self.browser = webdriver.Chrome(
                self.driver,
                options=chrome_options,
            )
            print("Scraping Module : Opening Chrome To Start Data Scraping")
            self.logger.debug("Scraping Module : Opening Chrome To Start Data Scraping")
            self.wait = WebDriverWait(self.browser, 20)
            return True, "driver session created "
        except WebDriverException as webDriverException:
            print(webDriverException)
            gink = "Issue with Chrome Driver. {0} visit https://chromedriver.chromium.org/downloads to download a new one".format(str(webDriverException), )
            print(gink)
            self.logger.error(gink)
            self.logger.error(gink)
            print(gink)
            return  False, str(webDriverException)
            # sys.exit(webDriverException)


    # Method to load URL
    def loadURL(self):
        # Opening Kijiji Website
        print("Opening webiste : " + self.site_url)
        try :
            self.browser.get(self.site_url)
            print("gotten url")
            self.browser.maximize_window()
            return True
        except:
            self.logger.error("Slow internet")
            return False


    # Method for Deleting Existing Site Cookies 
    def deleteCookies(self):
        # Deleting Existing Site Cookies
        self.browser.refresh()
        self.browser.delete_all_cookies()
        count_of_cookies = self.browser.get_cookies()
        time.sleep(10)
        while len(count_of_cookies) != 0:
            self.browser.delete_all_cookies()
            time.sleep(5)
        self.browser.refresh()
        print("deleted")


    # Method to set search Location parameters
    def setLocationSearch(self, city_name, province_name):
        try:
            location_box = self.wait.until(EC.element_to_be_clickable((By.ID, 'SearchLocationPicker')))
            location_box.click()
            time.sleep(40)
        except TimeoutException as timeoutException:
            self.logger.error("Issue while Finding the Location Box. Check your Internet Connection and Re-run the Program")
            print("Issue while Finding the Location Box. Check your Internet Connection and Re-run the Program")
            raise Exception("Issue while Finding the Location Box. Check your Internet Connection and Re-run the Program")

        try:
            address_box = self.wait.until(EC.element_to_be_clickable((By.NAME, 'address')))
            address_box.send_keys(city_name + ', ' + province_name)
            time.sleep(5)
            address_box.send_keys(' ')
            time.sleep(10)
            address_box.send_keys(Keys.ENTER)
            time.sleep(20)
        except TimeoutException as timeoutException:
            # address_box.send_keys(' ')
            
            # address_box.send_keys(Keys.ENTER)
            self.logger.error("Issue while Entering and Searching the Location. Check your Internet Connection and Re-run the Program")
            print("Issue while Entering and Searching the Location. Check your Internet Connection and Re-run the Program")
            raise Exception("Issue while Entering and Searching the Location. Check your Internet Connection and Re-run the Program")
            sys.exit()

        
        # try:
        #     time.sleep(10)
        #     full_address =self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'checkbox-792433335')))
        #     full_address.click()
        # except TimeoutException as timeoutException:
        #     self.logger.error("Issue while Getting the Full Address. Check your Internet Connection and Re-run the Program")
        #     print("Issue while Getting the Full Address. Check your Internet Connection and Re-run the Program")
        #     raise Exception("Issue while Getting the Full Address. Check your Internet Connection and Re-run the Program")

        time.sleep(20)
        try:
            applys =self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'submitButton-2124651659')))
            applys.click()
        except TimeoutException as timeoutException:
            self.logger.error("Issue while Submitting the Location. Check your Internet Connection and Re-run the Program")
            print("Issue while Submitting the Location. Check your Internet Connection and Re-run the Program")
            raise Exception("Issue while Submitting the Location. Check your Internet Connection and Re-run the Program")
            sys.exit()


    # Method to set Language to English
    def setLangauge(self):
        # Update Language to English
        try:
            language_update = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'headerLinkLanguage-203031519')))
            print(language_update.text)
            # if language_update.get_attribute('title') == 'English':
            if language_update.text.lower() == 'en':
                language_update.click()
        except TimeoutException as timeoutException:
            self.logger.error("Issue while updating Language to English. Check your Internet Connection and Re-run the Program")
            print("Issue while updating Language to English. Check your Internet Connection and Re-run the Program")
            sys.exit("Issue while updating Language to English. Check your Internet Connection and Re-run the Program")


    # Method for Splitting Search Keywords To Intitiate Searching
    def getKeyWords(self, search_words):
        keywords = search_words
        self.logger.debug("Scraping Module : Searching Keywords Are : " + str(keywords))
        print("Scraping Module : Searching Keywords Are : " + str(keywords))

        return keywords


    # Method to set key word in search field
    def setKeyWord (self, keyword):
        self.logger.debug("Scraping Module : Initiating Search For Keyword : " + str(keyword.strip()))
        print("Scraping Module : Initiating Search For Keyword : "+ str(keyword.strip()))

        # Getting Selenium Element for Search Input Box And Entering the Search Keyword
        try:
            search_box = self.wait.until(EC.element_to_be_clickable((By.ID, "SearchKeyword")))
            search_box.send_keys(keyword.strip())

        except TimeoutException as timeoutException:
            self.logger.error("Issue while Entering Advertisment Keyword. Check your Internet Connection and Re-run the Program")
            print("Issue while Entering Advertisment Keyword. Check your Internet Connection and Re-run the Program")
            raise Exception("Issue while Entering Advertisment Keyword. Check your Internet Connection and Re-run the Program" )

        # Getting Selenium Element for Search Submit Button And Clicking on it
        try:
            search_button = self.wait.until(
                EC.element_to_be_clickable((By.NAME, "SearchSubmit"))
            )
            search_button.click()
        except TimeoutException as timeoutException:
            self.logger.error("Issue while Proceeding with Searching for Advertisement Keyword. Check your Internet Connection and Re-run the Program")
            print("Issue while Proceeding with Searching for Advertisement Keyword. Check your Internet Connection and Re-run the Program")
            raise Exception("Issue while Proceeding with Searching for Advertisement Keyword. Check your Internet Connection and Re-run the Program")

        #self.waiting for Page to Load
        self.logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
        print("Scraping Module : waiting for Page to Load : Timeout 10 Seconds")
        time.sleep(20)


    # Method to get the links for specific Advertisments flters
    def getWantedAdvertisments(self, search_type):
        self.search_type_link = ''
        self.real_estate_link = ''
        self.for_rent_link = ''
        self.office_link = ''
        self.proceed_with_scraping = True 

        self.logger.debug("Scraping Module : Searching for : " + str(search_type) + " Advertisements")
        print("Scraping Module : Searching for : " + str(search_type) + " Advertisements")

        if search_type == "Wanted":
            self.search_type_link = self.extract_link("wantedSelection", "Wanted ")
        else:
            self.search_type_link = self.extract_link("offeringSelection", "Offering ")

        print(Self.search_type_link)
        if self.search_type_link != '':
            self.browser.get(self.search_type_link)
        else:
            self.proceed_with_scraping = False
            self.logger.debug("Scraping Module : Stopping Scraping as no " + str(search_type) + " advertisements found")
            print("Scraping Module : Stopping Scraping as no " + str(search_type) + " advertisements found")

        self.logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
        print("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
        time.sleep(10)

        # Getting Real Estate Link And Clicking It
        self.logger.debug("Scraping Module : Fetching Real Estate Advertisements")
        self.real_estate_link = self.extract_link("ChangeCategory", "Real Estate ")
        print(self.real_estate_link)
        if self.real_estate_link != '':
            self.browser.get(self.real_estate_link)
        else:
            self.proceed_with_scraping = False
            self.logger.debug("Scraping Module : Stopping Scraping as no Real Estate advertisements found")

        self.logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
        time.sleep(10)

        self.logger.debug("Scraping Module : Fetching Real Estate Advertisements For Rent")
        self.for_rent_link = self.extract_link("", "For Rent")
        if self.for_rent_link != '':
            self.browser.get(self.for_rent_link)
        else:
            self.proceed_with_scraping = False
            self.logger.debug("Scraping Module : Stopping Scraping as no Real Estate For Rent advertisements found")

        self.logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
        time.sleep(10)

        self.logger.debug("Scraping Module : Fetching Real Estate Advertisements For Commercial Spaces")
        self.commercial_space_link = self.extract_link("", "Commercial & Other")
        if self.commercial_space_link != '':
            self.browser.get(self.commercial_space_link)
        else:
            self.proceed_with_scraping = False
            self.logger.debug(
                "Scraping Module : Stopping Scraping as no Real Estate For Rent - Commericial And Office Space advertisements found")

        self.logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
        time.sleep(10)


    # Method to get the links for specific Advertisments flters
    def getAdType(self, search_type):
        self.search_type_link = ''
        self.proceed_with_scraping = False

        self.logger.debug("Scraping Module : Searching for : " + str(search_type) + " Advertisements")
        print("Scraping Module : Searching for : " + str(search_type) + " Advertisements")

        if search_type == "Wanted":
            self.search_type_link = self.extract_link("wantedSelection", "Wanted ")
        else:
            self.search_type_link = self.extract_link("offeringSelection", "Offering ")

        

        if self.search_type_link != '' and self.search_type_link is not None:
            self.logger.debug("Scraping Module : wanted link is : " + self.search_type_link)
            print("wanted link is : " + self.search_type_link)
            self.browser.get(self.search_type_link)
            self.proceed_with_scraping = True
        elif self.search_type_link is None:
            self.search_type_link = self.click_link(search_type)
            self.logger.debug("Scraping Module : wanted link is : " + self.search_type_link)
            print("wanted link is : " + self.search_type_link)
            self.browser.get(self.search_type_link)
            self.proceed_with_scraping = True
        else:
            self.proceed_with_scraping = False
            self.logger.debug("Scraping Module : Stopping Scraping as no " + str(search_type) + " advertisements found")
            print("Scraping Module : Stopping Scraping as no " + str(search_type) + " advertisements found")

        
        self.logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
        time.sleep(10)


    #method to trasvers pages collected
    def trasversePages(self, keyword, pages_traversed, total_pages, search_post_date, advertisment_links, current_advertisment_links, current_advertisements):
        # Looping Till All the Pages are Traversed
        self.logger.debug("Total pages : " + str(total_pages))
        print("Total pages : " + str(total_pages))
        while pages_traversed < total_pages:
        #while pages_traversed < 150:
            # Getting Selenium Element for Advertisement
            advertisements = self.browser.find_elements_by_class_name("regular-ad")
            print(len(advertisements))

            for ad in advertisements:
                wanted_ad = False
                try:
                    ad_date = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "date-posted")))
                    ad_date = ad_date.text
                except TimeoutException as timeoutException:
                    self.logger.debug("Could not find date poster")
                    continue

                if "ago" in ad_date:
                    wanted_ad = True
                elif "Yesterday" in ad_date:
                    today = date.today()
                    yesterday = today - timedelta(days=1)
                    if yesterday >= search_post_date:
                        wanted_ad = True
                else:
                    ad_posted_date = datetime.strptime(ad_date, "%d/%m/%Y").date()
                    if ad_posted_date >= search_post_date:
                        wanted_ad = True

                if wanted_ad:
                    advertisment_links.add(ad.find_element_by_tag_name("a").get_attribute("href"))
                    current_advertisment_links.append(ad.find_element_by_tag_name("a").get_attribute("href"))

            pages_traversed += 1
            self.logger.debug("Scraping Module : Pages Traversed So Far : " + str(pages_traversed))
            print("Scraping Module : Pages Traversed So Far : " + str(pages_traversed))
            links_processed = len(current_advertisment_links)
            self.logger.debug("Scraping Module : Links Processed So Far : " + str(links_processed))
            print("Scraping Module : Links Processed So Far : " + str(links_processed))
            next_page_url = ""

            if str(pages_traversed) != str(total_pages) and str(links_processed) == str(current_advertisements):
                try:
                    pagination_element = self.browser.find_element_by_class_name("pagination")
                except:
                    pagination_element = ""


                if pagination_element != "":
                    for link in pagination_element.find_elements_by_tag_name("a"):
                        if "Next" == link.get_attribute("title"):
                            next_page_url = link.get_attribute("href")
                            break
                print(next_page_url)
                self.browser.get(next_page_url)
            else:
                break

        self.logger.debug("Scraping Module : Total Links for : " + str(keyword) + " is : " + str(len(current_advertisment_links)))
        print("Scraping Module : Total Links for : " + str(keyword) + " is : " + str(len(current_advertisment_links)))
        # Getting Search Box Selenium Element to Clear its Text before Inputting Next Text
        search_box = self.wait.until(EC.element_to_be_clickable((By.ID, 'SearchKeyword')))
        time.sleep(2)
        search_box.clear()

        return advertisment_links


    # Method to start search loop 
    def search(self, keyword, date_in_property):
        # Search Started Using For Each Loop
        # proceed_with_scraping = True
        try:
            # Getting Selenium Element for Total No Of Results
            showing = self.browser.find_element_by_class_name("resultsShowingCount-1707762110")
            address = self.browser.find_element_by_class_name("label-1952128162")
            showing_text = showing.text
            self.logger.debug(
                "Scraping Module : Search Result For  : "
                + str(keyword.strip())
                + " : is : "
                + str(showing_text)
            )
            print(
                "Scraping Module : Search Result For  : "
                + str(keyword.strip())
                + " : is : "
                + str(showing_text)
            )
            if showing_text != "No results":
                print(showing_text)
                total_advertisements = showing_text.split(" ")[5]
                total_advertisements = total_advertisements.replace(",", "")
                self.logger.debug(
                    "Scraping Module : Total Advertisements Fetched : "
                    + str(total_advertisements)
                )
                print(
                    "Scraping Module : Total Advertisements Fetched : "
                    + str(total_advertisements)
                )
                current_advertisements = showing_text.split(" ")[3]
                self.logger.debug(
                    "Scraping Module : Current Advertisements Fetched : "
                    + str(current_advertisements)
                )
                print(
                    "Scraping Module : Current Advertisements Fetched : "
                    + str(current_advertisements)
                )
                total_pages = math.ceil(
                    int(total_advertisements) / int(current_advertisements)
                )
                self.logger.debug(
                    "Scraping Module : Total Pages To Be Parsed : "
                    + str(total_pages)
                )
                print(
                    "Scraping Module : Total Pages To Be Parsed : "
                    + str(total_pages)
                )
            else:
                self.logger.debug("Scraping Module : No Appropriate Advertisements Found")
                self.logger.debug("Scraping Module : Moving On to Other Keyword If Any")
                print("Scraping Module : No Appropriate Advertisements Found")
                print("Scraping Module : Moving On to Other Keyword If Any")
                total_pages = 0
                current_advertisements = 0

        except Exception as e:
            self.logger.debug("Scraping Module : Exception in Fetching Total No Of Pages")
            print("Scraping Module : Exception in Fetching Total No Of Pages")
            print(e)
            print("Scraping Module : System Existing")
            total_pages = 0
            sys.exit()

        self.logger.debug("Scraping Module : Total Pages = " + str(total_pages))
        print("Scraping Module : Total Pages = " + str(total_pages))
        # Fetching Advertisement Links
        advertisment_links = set()
        current_advertisment_links = []
        pages_traversed = 0

        # Getting Configured Date from the Configuration
        search_post_date = datetime.strptime(date_in_property, "%d/%m/%Y").date()
        self.logger.debug("Scraping Module : Configured Search Date is : " + str(search_post_date))
        print( "Scraping Module : Configured Search Date is : " + str(search_post_date))

        if date_in_property == "01/01/1970":
            self.logger.debug("Scraping Module : Calculating Previous 30 Days to Start Searching")
            print("Scraping Module : Calculating Previous 30 Days to Start Searching")
            today = date.today()
            search_post_date = today - timedelta(days=30)
            self.logger.debug("Scraping Module : Calculated Search Date is : " + str(search_post_date))
            print("Scraping Module : Calculated Search Date is : " + str(search_post_date))

        if current_advertisements != 0:
            al  = self.trasversePages(keyword, pages_traversed, total_pages, search_post_date, advertisment_links, current_advertisment_links, current_advertisements)
            return al
        else :
            return []
        


    # Function to start scrapping set URL
    #calss all the methods needed
    def startScrape(self, args):
        state, msg = self.initBrowser()
        if state:
            pa, ca, ta, sk          = self.getParameters(args)
            st, dp, fip, pn, cn, sv = self.getLocationVariables(pa, ca, ta)
            self.deleteCookies()
            url_is_loaded           = self.loadURL()

            if url_is_loaded:
                self.setLocationSearch(cn, pn)
                self.logger.debug("Scraping Module : Location Set")
                print("Scraping Module : Location Set")
                self.setLangauge()
                self.logger.debug("Scraping Module : Language Set")
                print("Scraping Module : Language Set")

                # Splitting Search Keywords To Intitiate Searching
                keywords                = self.getKeyWords(sk)
                for keyword in keywords:
                    self.setKeyWord(keyword)
                    self.logger.debug("Scraping Module : Keyword Set")
                    print("Scraping Module : Keyword Set")
                    self.getAdType(st)
                    self.logger.debug("Scraping Module : " + st + " Advertisement Type Set")
                    print("Scraping Module : " + st + " Advertisement Type Set")
            #     self.getWantedAdvertisments(st)
                    if self.proceed_with_scraping:
                        advertisment_links      = self.search(keyword, dp)
                        self.logger.debug("Scraping Module : Starting Data Scraping")
                        print("Scraping Module : Starting Data Scraping")
                        extract = Extract()
                        self.logger.debug("Scraping Module : Final Processing For All Advertisements In Progress")
                        print("Scraping Module : Final Processing For All Advertisements In Progress")
                        current_timestamp       = extract.extract_data(self.browser,keywords,  advertisment_links, fip, self.handleProperties, pn, cn) 
                        updated_date            = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
                        print("here 1")
                        location_dictionary     = self.setLocationVariables(sv[0], sv[1], sv[2], sv[3], sv[4], sv[5], sv[6], sv[7], sv[8], current_timestamp, updated_date)
                        print("here 2")
                        self.openFile("w", location_dictionary)
                        print("here 3")
                        self.browser.close()
                        print("here 4")
                        self.browser.quit()
                        print("here 5")
                        return advertisment_links
                    else:
                        self.browser.close()
                        self.browser.quit()
                        self.logger.error("Scraping Module : No Data to scrape")
                        sys.exit("No Data to scrape")

            else:
                self.logger.error("Scraping Module : Slow Internet")
                print("slow internet")
                sys.exit("slow internet")
        else:
            sys.exit(msg)

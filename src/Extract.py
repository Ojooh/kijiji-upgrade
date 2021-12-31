import time
from datetime import datetime
import csv
import re
import pathlib
import os


class Extract:

    def __init__(self):
        self.current_timestamp          = 0
        self.row                        = []
        self.count                      = 0
        self.addey                      = 0
        self.project_directory_path     = pathlib.Path(__file__).parents[1]
        self.data_directory_path        = str(self.project_directory_path) + "/result/"
        if not os.path.exists(self.data_directory_path):
            os.mkdir(self.data_directory_path)
        

    def extract_data(self, browser, keywords, advertisment_links, finalTimestamp, fetchProperties, province_name, city_name):
        kawey = '-'.join(keywords)
        print(kawey)
        if finalTimestamp != "0":
            final_timestamp = datetime.strptime(finalTimestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    
        city_name_split_list = city_name.split(' ')
        final_city_name = ''

        for name in city_name_split_list:
            if name != "/":
                if final_city_name != '':
                    final_city_name = final_city_name + "-"
                final_city_name = final_city_name + name.strip()

        
        fileName = datetime.now().strftime(str(self.data_directory_path) + "Data_" + province_name + "_" + final_city_name + "_" + '_%d_%m_%Y_%H_%M_%S' + '.csv')
        print(fileName)

        with open(fileName, 'w+', newline='', encoding='utf-8') as csvfile:
            output_csv = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
            self.row.append("Unique Id")
            self.row.append("Time Posted")
            self.row.append("Page Link")
            self.row.append("Title")
            self.row.append("Description")
            self.row.append("Address")
            self.row.append("City")
            self.row.append("Postal Code")
            self.row.append("Phone No")
            self.row.append("Email")
            self.row.append("Province Name")
            self.row.append("City Name")
            self.row.append("Keywords")

            output_csv.writerow(self.row)
            self.row.clear()
            self.count = 0

            if len(advertisment_links) > 0 :
                print("getting the links")
                for link in advertisment_links:
                    print("current url : " + link);
                    print("total links : " + str(len(advertisment_links)))
                    to_be_added = False
                    to_be_added_error = False
                    browser.get(link)
                    time.sleep(2)

                    
                    try:
                        date_element        = browser.find_element_by_class_name("datePosted-383942873")
                        date_span_element   = date_element.find_element_by_tag_name("time")
                        timestamp           = date_span_element.get_attribute("datetime")
                        formatted_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                    except Exception:
                        to_be_added_error = True
                        timestamp = 0
                        formatted_timestamp = 0

                    if not to_be_added_error:
                        if self.current_timestamp == 0:
                            self.current_timestamp = timestamp

                        if finalTimestamp == "0":
                            to_be_added = True
                        elif finalTimestamp != "0":
                            if formatted_timestamp > final_timestamp:
                                to_be_added = True
                    else:
                        to_be_added = True

                    if to_be_added:
                        self.addey += 1
                        print("current url : " + link)
                        page_link   = link
                    
                        try:
                            title           = browser.find_element_by_class_name("title-2323565163")
                            description     = browser.find_element_by_class_name("descriptionContainer-3261352004").find_element_by_tag_name("div").find_element_by_tag_name("p")
                            address         = browser.find_element_by_class_name("locationContainer-2867112055").find_element_by_class_name("address-3617944557")
                            # description     = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "descriptionContainer-3544745383")).EC.presence_of_element_located((By.TAG_NAME, "div")))
                            title           = title.text
                            description     = description.text
                            address         = address.text
                        except:
                            description     = ""
                            title           = ""
                            address         = ""

                        
                        postal_code_pattern = re.search("[A-Za-z][0-9][A-Za-z](\s){0,1}[0-9][A-Za-z][0-9]", address)

                        if postal_code_pattern != None:
                            codes = postal_code_pattern.group()
                        else:
                            codes = ''

                        city = ((address.upper().replace(codes.upper(), '').replace('CANADA', '')).replace(",", '')).strip()

                        email_pattern   = re.compile('\w+@\w+\.[a-z]{3}')
                        emails          = email_pattern.findall(description)
                        mails           = ''

                        if len(emails) > 0:
                            for email in emails:
                                mails += email
                                mails += "\n"

                        phone_number_pattern = re.compile('[0-9]{3}?[-\s]?[0-9]{3}[-\s]?[0-9]{4}')
                        phone_numbers = phone_number_pattern.findall(description)
                        numbers = ''
                        if len(phone_numbers) > 0:
                            for phone_number in phone_numbers:
                                numbers += phone_number
                                numbers += "\n"

                        link_attributes = page_link.split('/')

                        self.row.append(link_attributes[len(link_attributes) - 1])
                        self.row.append(formatted_timestamp)
                        self.row.append(page_link)
                        self.row.append(title)
                        self.row.append(description)
                        self.row.append(address)
                        self.row.append(city)
                        self.row.append(codes)
                        self.row.append(numbers)
                        self.row.append(mails)
                        self.row.append(province_name)
                        self.row.append(city_name)
                        self.row.append(kawey)

                        output_csv.writerow(self.row)
                        print("added row : " + str(self.addey))
                        self.row.clear()
                        
                        self.count += 1

                        if self.count == 10:
                            self.count = 0
                            print("Extract Module : Process Still Running.....")

            else:
                print("no links")
                return 0
        print("done")  
        return self.current_timestamp

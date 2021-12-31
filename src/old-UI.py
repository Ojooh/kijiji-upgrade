import tkinter
import subprocess
import threading
from tkinter import ttk
from selenium.common.exceptions import TimeoutException, WebDriverException
import json


class WebScrapingWindow:

    def __init__(self):
        # Initializing Application Window
        self.window                 = tkinter.Tk()
        self. window.title("Kijiji Web Scraping")
        self.windowWidth            = self.window.winfo_reqwidth()
        self.windowHeight           = self.window.winfo_reqheight()
        self.window['background']   = '#e6e6e6'
        self.keywordsCount = 8
        self.count = 0
        self.keywords = {}



    # Function to destroy window
    def destroy_window(self):
        self.window.destroy()


    #Funcion to get province and city dict
    def getDict(self):
        with open ("location_dict.json", "r") as js:
            data            = json.load(js)
            province_dict   = data[0]["province_dict"]
            city_dict       = data[1]["city_dict"]

        return province_dict, city_dict


    # Function to run a sub Process for executing scrapping
    def subProcess(self, province, city, type, keyword):
        try:
            subprocess.check_call(
                "python initScrapper.py " + province + " " + city + " w " + keyword, shell=True
            )
            label = ttk.Label(
                self.window, 
                text="Process Completed", 
                font=("Calibri", 15)
            ).place(relx="0.35", rely="0.7")

            self.progressBar.destroy()
            self.progressBBar = ttk.Progressbar(
                self.window, 
                orient='horizontal', 
                length=400, 
                mode='determinate'
            )
            self.progressBBar.place(relx="0.1", rely="0.8")
            self.progressBBar['value'] = 100

            bbtn = ttk.Button(
                self.window, 
                text="Ok", 
                command=self.destroy_window
            ).place(relx="0.4", rely="0.9")

        except subprocess.CalledProcessError:
            label = ttk.Label(
                self.window, 
                text="Error Occured. Please check the Logs", 
                font=("Calibri", 15)
            ).place(relx="0.25", rely="0.7")
            self.progressBar.destroy()

            self.progressBBar = ttk.Progressbar(
                self.window, 
                orient='horizontal', 
                length=400, 
                mode='determinate'
            )
            self.progressBBar.place(relx="0.1", rely="0.8")

            self.progressBBar['value'] = 100

            bbtn = ttk.Button(
                self.window, 
                text="Ok", 
                command=self.destroy_window
            ).place(relx="0.4", rely="0.9")

   
    # Function to add Keyword
    def addKeyword(self):
        # global keywordsCount
        # global count
        if self.keywordsCount < 10:
            self.count += 1
            self.keywordsCount += 1
            self.keywords[str(self.count)] = ttk.Entry(
                self.window, 
                width=35
            )
            self.keywords[str(self.count)].grid(column=1, row=self.keywordsCount, pady=10)


    # Function to enable province
    def enableProvince(self, event):
        ttk.Label(
            self.window, 
            text="Province :", 
            font=("Calibri", 15)
        ).grid(column=0, row=6, padx=10, pady=10)
        print(self.province_choosen)
        self.province_choosen.grid(column=1, row=6)
        self.province_choosen.current()


    # Function to enable Cities
    def enableCities(self, event):
        if self.province_choosen.get().strip() == "Alberta":
            self.city_choosen['values'] = (
             ' Calgary', ' Edmonton Area'
        )
        elif self.province_choosen.get().strip() == "British Columbia":
            self.city_choosen['values'] = (
                ' Greater Vancouver Area', ' Kelowna', ' Nanaimo', ' Victoria',' Whistler' 
            )
        elif self.province_choosen.get().strip() == "Manitoba":
            self.city_choosen['values'] = (
                ' Winnipeg'
            )
        elif self.province_choosen.get().strip() == "Nova Scotia":
            self.city_choosen['values'] = (
                ' Halifax',
            )
        elif self.province_choosen.get().strip() == "Ontario":
            self.city_choosen['values'] = (
                ' Barrie', ' Hamilton', ' Kitchener Area',
                ' Ottawa / Gatineau Area',
                ' Toronto (GTA)'
            )
        elif self.province_choosen.get().strip() == "Qu\u00e9bec":
            self.city_choosen['values'] = (
                ' Greater Montr\u00e9al',' Qu\u00e9bec City'
            )
        elif self.province_choosen.get().strip() == "Saskatchewan":
            self.city_choosen['values'] = (
                ' Regina Area',
            )
        # City Label And ComboBox
        # if self.province_choosen.get().strip() == "Alberta":
        #     self.city_choosen['values']= (
        #         ' Banff / Canmore', ' Calgary', ' Edmonton Area', ' Fort McMurray', ' Grande Prairie', ' Lethbridge',
        #         ' Lloydminster', ' Medicine Hat', ' Red Deer'
        #     )
        # elif self.province_choosen.get().strip() == "British Columbia":
        #     self.city_choosen['values']= (
        #         ' Cariboo Area', ' Comox Valley Area', ' Cowichan Valley / Duncan', ' Cranbrook', ' Fraser Valley',
        #         ' Greater Vancouver Area',
        #         ' Kamloops', ' Kelowna', ' Nanaimo', ' Nelson', ' Peace River Area', ' Port Alberni / Oceanside',
        #         ' Port Hardy / Port McNeill', ' Powell River District',
        #         ' Prince George', ' Revelstoke', ' Skeena-Bulkley Area', ' Sunshine Coast', ' Vernon', ' Victoria',
        #         ' Whistler'
        #     )
        # elif self.province_choosen.get().strip() == "Manitoba":
        #     self.city_choosen['values']= (
        #         ' Brandon Area', ' Flin Flon', ' Thompson', ' Winnipeg'
        #     )
        # elif self.province_choosen.get().strip() == "New Brunswick":
        #     self.city_choosen['values']= (
        #         ' Bathurst', ' Edmundston', ' Fredericton', ' Miramichi', ' Moncton', ' Saint John'
        #     )
        # elif self.province_choosen.get().strip() == "Newfoundland":
        #     self.city_choosen['values']= (
        #         ' Corner Brook', ' Gander', ' Labrador', " St. John's", ' Moncton', ' Saint John'
        #     )
        # elif self.province_choosen.get().strip() == "Nova Scotia":
        #     self.city_choosen['values']= (
        #         ' Annapolis Valley', ' Bridgewater', ' Cape Breton', " Halifax", ' New Glasgow', ' Truro', ' Yarmouth'
        #     )
        # elif self.province_choosen.get().strip() == "Ontario":
        #     self.city_choosen['values']= (
        #         ' Barrie', ' Belleville Area', ' Brantford', " Brockville", ' Chatham-Kent', ' Cornwall',
        #         ' Guelph', ' Hamilton', ' Kapuskasing', ' Kenora', ' Kingston Area', ' Kitchener Area',
        #         ' Leamington', ' London', ' Muskoka', ' Norfolk County', ' North Bay', " Ottawa / Gatineau Area",
        #         ' Owen Sound', ' Peterborough Area',
        #         ' Renfrew County Area', ' Sarnia Area', ' Sault Ste. Marie', ' St. Catharines', ' Sudbury', ' Thunder Bay',
        #         ' Timmins', ' Toronto (GTA)', ' Windsor Region', ' Woodstock'
        #     )
        # elif self.province_choosen.get().strip() == "Prince Edward Island":
        #     self.city_choosen['values']= (
        #         ' Prince Edward Island'
        #     )
        # elif self.province_choosen.get().strip() == "Qu\u00e9bec":
        #     self.city_choosen['values']= (
        #         ' Abitibi-T\u00e9miscamingue', ' Baie-Comeau', ' Centre-du-Quebec', " Chaudi\u00e8re-Appalaches",
        #         ' Chibougamau / Northern Qu\u00e9bec', ' Gasp\u00e9',
        #         ' Granby', ' Greater Montr\u00e9al', ' Lanaudi\u00e8re', ' Laurentides', ' Mauricie', ' Qu\u00e9bec City',
        #         ' Rimouski / Bas-St-Laurent', ' Saguenay-Lac-Saint-Jean', ' Saint-Hyacinthe', ' Saint-Jean-sur-Richelieu',
        #         ' Sept-\u00celes', ' Sherbrooke'
        #     )
        # elif self.province_choosen.get().strip() == "Saskatchewan":
        #     self.city_choosen['values']= (
        #         ' La Ronge', ' Meadow Lake', ' Nipawin', " Prince Albert", ' Regina Area', ' Saskatoon', ' Swift Current'
        #     )
        # elif self.province_choosen.get().strip() == "Territories":
        #     self.city_choosen['values']= (
        #         ' Northwest Territories', ' Nunavut', ' Yukon'
        #     )

        ttk.Label(
            self.window, 
            text="City :", 
            font=("Calibri", 15)
        ).grid(column=0, row=7, padx=10, pady=10)

        self.city_choosen.grid(column=1, row=7)
        self.city_choosen.current()


    #Function to enable Button
    def enableButton(self, event):
        ttk.Label(
            self.window, 
            text="Keyword :", 
            font=("Calibri", 15)
        ).grid(column=0, row=8, padx=10, pady=10)

        self.keywords[str(self.count)] = ttk.Entry(
            self.window, 
            width=35
        )

        self.keywords[str(self.count)].grid(column=1, row=8)

        bbtn = ttk.Button(
            self.window, 
            text="Add", 
            command=self.addKeyword
        )

        bbtn.place(relx="0.1", rely="0.5")
        self.btn.place(relx="0.4", rely="0.7")


    # Function to execute Scrapping
    def execute_scraping(self):
        self.btn.destroy()
        label = ttk.Label(
            self.window, 
            text="Process Running......", 
            font=("Calibri", 15)
        ).place(relx="0.35", rely="0.7")

        self.progressBar = ttk.Progressbar(
            self.window, 
            orient='horizontal', 
            length=400, 
            mode='determinate'
        )
        self.progressBar.place(relx="0.1", rely="0.8")
        self.progressBar.start(10)

        self.finalKeywords = ''
        if self.count >= 0:
            self.finalKeywords += self.keywords["0"].get()
        if self.count >= 1:
            self.finalKeywords += ','
            self.finalKeywords += self.keywords["1"].get()
        if self.count == 2:
            self.finalKeywords += ','
            self.finalKeywords += self.keywords["2"].get()

    
        if self.advertisement_type.get().strip() == "Wanted":
            province_dict, city_dict = self.getDict()

            province    = str(province_dict[self.province_choosen.get().strip()])
            city        =  str((city_dict[province_dict[self.province_choosen.get().strip()]])[self.city_choosen.get().strip()]) 
            ad_type     = " w "
            kyword      = str(self.finalKeywords).replace(" ", "_")
            scriptRun = threading.Thread(target=self.subProcess, args=(province, city, ad_type, kyword))
            scriptRun.start()

        elif self.advertisement_type.get().strip() == "Offering":
            province_dict, city_dict = self.getDict()
            
            province    = str(province_dict[self.province_choosen.get().strip()]) 
            city        = str((city_dict[province_dict[self.province_choosen.get().strip()]])[self.city_choosen.get().strip()])
            ad_type     = " o "
            kyword      = str(self.finalKeywords)
            scriptRun = threading.Thread(target=self.subProcess, args=(province, city, ad_type, kyword))
            scriptRun.start()
            

    # Function to position the window at the center of your screen
    def position_window(self):
        # Gets both half the screen width/height and window width/height
        positionRight   = int(self.window.winfo_screenwidth() / 2 - self.windowWidth)
        positionDown    = int(self.window.winfo_screenheight() / 2 - self.windowHeight)

        # Positions the window in the center of the page.
        self.window.geometry("+{}+{}".format(positionRight, positionDown))
        self.window.geometry('500x400')


    # Function for Advertisement Type : Dropdown, Values And Positioning
    def advertiment_type_positioning(self):
        self.advertisement_lbl = ttk.Label(
            self.window, 
            text="Advertisement Type :", 
            font=("Calibri", 15)
        ).grid(column=0, row=5, padx=10, pady=10)

        self.advertisement_type = ttk.Combobox(
            self.window, 
            width=35, 
            height=30, 
            textvariable=tkinter.StringVar(), 
            state="readonly"
        )
        self.advertisement_type.bind("<<ComboboxSelected>>", self.enableProvince)
        self.advertisement_type['values'] = (' Wanted', ' Offering')
        self.advertisement_type.grid(column=1, row=5)
        self.advertisement_type.current()


    # Function for rovince : Dropdown, Values, Positioning and Method Calling To Enable Cities
    def province (self):
        self.province_choosen = ttk.Combobox(
           self.window, 
           width=35, 
           height=30, 
           textvariable=tkinter.StringVar(), 
           state="readonly"
        )
        self.province_choosen.bind("<<ComboboxSelected>>", self.enableCities)
        self.province_choosen['values'] = (
            ' Alberta', ' British Columbia', ' Manitoba', ' Nova Scotia',
            ' Ontario', ' Qu\u00e9bec', ' Saskatchewan'
        )

        # self.province_choosen['values'] = (
        #     ' Alberta', ' British Columbia', ' Manitoba', ' New Brunswick', ' Newfoundland', ' Nova Scotia',
        #     ' Ontario', ' Prince Edward Island', ' Qu\u00e9bec', ' Saskatchewan', ' Territories'
        # ) 


    # Function for City : Dropdown, Values, Positioning
    def city (self):
        self.city_choosen = ttk.Combobox(
            self.window, 
            width=35, 
            height=30, 
            textvariable=tkinter.StringVar(), 
            state="readonly"
        )
        
        self.city_choosen.bind("<<ComboboxSelected>>", self.enableButton)

        self.btn = ttk.Button(
            self.window, 
            text="Start", 
            command=self.execute_scraping
        )
        


    def window_loop(self):
        self.position_window()
        self.advertiment_type_positioning()
        self.province()
        self.city()
        self.window.mainloop()





ws  = WebScrapingWindow()

ws.window_loop()
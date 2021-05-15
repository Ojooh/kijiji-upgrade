import json 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image  
# import subprocess
# import threading
# from selenium.common.exceptions import TimeoutException, WebDriverException
LARGEFONT =("Verdana", 35)
PATHS = {"logo" : "img/kijiji.png", "startBtn" : "img/startBtn.png", "searchBtn" : "img/searchBtn.png", "clearBtn" : "img/clear.png",}
PROVINCES = (
            ' Alberta', ' British Columbia', ' Manitoba', ' Nova Scotia',
            ' Ontario', ' Qu\u00e9bec', ' Saskatchewan'
        )


# mainApp Window
class kijijiApp(tk.Tk):
    def __init__(self):
        # Initializing Application Window
        tk.Tk.__init__(self)
        # self.window                 = tk.Tk()
        self.windowWidth            = self.winfo_reqwidth()
        self.windowHeight           = self.winfo_reqheight()
        self['background']   = '#0D0C52'
        self.title("Kijiji AutoBot")
        self.resizable(False, False)
        self.window_loop()
        


    # Function to position the window at the center of your screen
    def position_window(self, geo):
        # Gets both half the screen width/height and window width/height
        # positionRight   = int(self.winfo_screenwidth() /2  - self.windowWidth)
        # positionDown    = int(self.winfo_screenheight() / 2 - self.windowHeight)
        positionRight   = int(self.winfo_screenwidth()  * 0.3)
        positionDown    = int(self.winfo_screenheight() * 0.1)
       


        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
        self.geometry(geo)


    # Function to position Frame
    def position_Frame(self):
        self.container = tk.Frame(
            self, 
            bg="#0D0C52",
            bd = 0,
            width=568,
            height=488
        )
        self.container.pack()


    #show frames
    def show_frame(self, frame_class, geo):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        self.position_window(geo)
        if self.container is not None:
            self.container.destroy()
        self.container = new_frame
        self.container.pack(side = "top", fill = "both", expand = True)


    def window_loop(self):
        self.position_window('568x488')
        self.position_Frame()
        # self.init_frame()
        self.show_frame(WelcomePage, '568x488')
        self.mainloop()



# welocmeWindow Frame
class WelcomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(
            self, 
            master, 
            bg="#0D0C52",
            bd = 0,
            width=568,
            height=488
        )

        self.position_headerText()
        self.position_logoImg()
        self.position_StartBtn(master)
         
    # Function to position the text at the center of the window
    def position_headerText(self):
        x_axis = 568 - 400
        y_axis = 488 - 470
        self.headerTxt = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text="KIJIJI AUTOBOT", 
            font=("Roboto Condensed", 20, "bold")
        ).place(x=x_axis, y=y_axis)

    # Function to position logo
    def position_logoImg(self):
        x_axis = 0
        y_axis = 488 - 425
        self.c = tk.Canvas(
            self, 
            bg = '#0D0C52',
            bd = 0,
            highlightthickness=0,
            width = 563, 
            height = 280
        )
        self.img_1 = ImageTk.PhotoImage(Image.open(PATHS["logo"]).resize((265, 265), Image.ANTIALIAS)) 
        # print(img) 
        self.c.create_image(150, 20, anchor="nw", image=self.img_1)
        self.c.image = self.img_1
        self.c.place(x=x_axis, y=y_axis)
        self.c.image = self.img_1
       
    # Function to position button
    def position_StartBtn(self, master):
        # Placement axis
        x_axis = 568 - 368
        y_axis = 488 - 80
        # Add Image
        self.img_2 = ImageTk.PhotoImage(Image.open(PATHS["startBtn"]))
        # Create button and image
        self.startBtn = tk.Button(
            self, 
            image=self.img_2,
            bd = 0,
            command=lambda: master.show_frame(FormPage, '739x668')
        )
        self.startBtn.image = self.img_2
        self.startBtn.place(x=x_axis, y=y_axis)
        self.startBtn.image = self.img_2


# formWindow Frame
class FormPage(tk.Frame):
     
    def __init__(self, master):
        tk.Frame.__init__(
            self, 
            master, 
            bg="#0D0C52",
            bd = 0,
            width=739,
            height=668
        )
        self.locations = []
        self.count = 0

        self.position_headerSection()
        self.position_KeyWordSection()
        self.position_Dropdowns()
        self.position_Table()
        self.position_clearBtn()
        self.position_searchBtn()


     # Function to create and position the text and logo at the center of the window
    def position_headerSection(self):
        x_axis = 739 - 420
        y_axis = 668 - 658
        self.headerTxt = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text="KIJIJI AUTOBOT", 
            font=("Roboto Condensed", 20, "bold")
        ).place(x=x_axis, y=y_axis)

        self.c2 = tk.Canvas(
            self, 
            bg = '#0D0C52',
            bd = 0,
            highlightthickness=0,
            width = 70, 
            height = 50
        )
        x_axis = 739 - 490
        y_axis = 668 - 668
        self.img_3 = ImageTk.PhotoImage(Image.open(PATHS["logo"]).resize((42, 42), Image.ANTIALIAS)) 
        # print(img) 
        self.c2.create_image(20, 10, anchor="nw", image=self.img_3)
        self.c2.image = self.img_3
        self.c2.place(x=x_axis, y=y_axis)
        self.c2.image = self.img_3
    

    #Function to create and position keyword Input
    def position_KeyWordSection(self):
        x_axis = 739 - 417
        y_axis = 668 - 598
        self.keywordLbl = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text="Keyword :", 
            font=("Roboto Condensed", 16)
        ).place(x=x_axis, y=y_axis)

        x_axis = 739 - 699
        y_axis = 668 - 573

        self.keywordInput = ttk.Entry(
            self, 
            background="#0D0C52",
            foreground = "#0D0C52",
            font=("Roboto Condensed", 16),
            width = 54,
        ).place(x=x_axis, y=y_axis)

        x_axis = 739 - 500
        y_axis = 668 - 543
        self.infoLbl = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text=" Please seperate multiple kewords with a comma :", 
            font=("Roboto Condensed", 10)
        ).place(x=x_axis, y=y_axis)

    
    #Function to create and position provinces and city
    def position_Dropdowns(self):
        x_axis = 739 - 620
        y_axis = 668 - 500
        self.provinceLbl = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text=" Province :", 
            font=("Roboto Condensed", 16)
        ).place(x=x_axis, y=y_axis)

        x_axis = 739 - 699
        y_axis = 668 - 475
        self.provinceInput = ttk.Combobox(
            self, 
            background="#0D0C52",
            foreground = "#0D0C52",
            text=" Province :", 
            font=("Roboto Condensed", 16),
            textvariable=tk.StringVar(), 
            state="readonly",
            values = PROVINCES
        )
        self.provinceInput.bind("<<ComboboxSelected>>", self.displayCities)
        self.provinceInput.place(x=x_axis, y=y_axis)
        

        x_axis = 739 - 200
        y_axis = 668 - 500
        self.cityLbl = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text=" City :", 
            font=("Roboto Condensed", 16)
        ).place(x=x_axis, y=y_axis)

        x_axis = 739 - 310
        y_axis = 668 - 475
        self.cityInput = ttk.Combobox(
            self, 
            background="#0D0C52",
            foreground = "#0D0C52",
            text=" Province :",
            textvariable=tk.StringVar(), 
            state="readonly", 
            font=("Roboto Condensed", 16)
        )
        self.cityInput.bind("<<ComboboxSelected>>", self.ConfirmLocation)
        self.cityInput.place(x=x_axis, y=y_axis)


    # Function to position location tables
    def position_Table(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview",
            background = "#C4C4C4",
            foreground = "black",
            rowheight = 20,
            fieldbackground = "#C4C4C4",
        )

        self.style.map (
            "Treeview",
            background= [('selected' , '#0D0C52')]
        )
        x_axis = 739 - 699
        y_axis = 668 - 425

        self.tbl = ttk.Treeview(
            self, 
            show='headings', 
            height="10",
           
        )

        self.tbl['columns']=('s/n', 'Province', 'City')
        self.tbl.column('s/n',  width=80, anchor=tk.CENTER)
        self.tbl.column('Province',  width=272, anchor=tk.CENTER)
        self.tbl.column('City',  width=272, anchor=tk.CENTER)

        # define headings
        self.tbl.heading('s/n', text='s/n')
        self.tbl.heading('Province', text='Province')
        self.tbl.heading('City', text='City')

        self.tbl.bind("<Double-1>", self.removeRecord)

        self.tbl.place(x=x_axis, y=y_axis)

        x_axis = 739 - 70
        y_axis = 668 - 425
        self.scrollbar = tk.Scrollbar(
            self, 
            bg="#0D0C52",
            activebackground="#0D0C52",
            orient=tk.VERTICAL, 
            command=self.tbl.yview,
           
            # height="10",
        )
        self.tbl.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=x_axis, y=y_axis, height="228")


    #Function to create and position clearbtn btn
    def position_clearBtn(self):
        # Placement axis
        x_axis = 739 - 500
        y_axis = 668 - 180
        # Add Image
        self.img_4 = ImageTk.PhotoImage(Image.open(PATHS["clearBtn"]))
        # Create button and image
        self.clearBtn = tk.Button(
            self, 
            image=self.img_4,
            bd = 0,
            bg="#0D0C52",
            command=self.clearRecords
        )
        self.clearBtn.image = self.img_4
        self.clearBtn.place(x=x_axis, y=y_axis, height="30")
        self.clearBtn.image = self.img_4


    #Function to create and position search btn
    def position_searchBtn(self):
        # Placement axis
        x_axis = 739 - 470
        y_axis = 668 - 75
        # Add Image
        self.img_5 = ImageTk.PhotoImage(Image.open(PATHS["searchBtn"]))
        # Create button and image
        self.searchBtn = tk.Button(
            self, 
            image=self.img_5,
            bd = 0,
        )
        self.searchBtn.image = self.img_5
        self.searchBtn.place(x=x_axis, y=y_axis)
        self.searchBtn.image = self.img_5

  
    #Function to display cities on province selection
    def displayCities(self, event):
        
        if self.provinceInput.get().strip() == "Alberta":
            self.cityInput["values"] = (' Calgary', ' Edmonton Area')
        elif self.provinceInput.get().strip() == "British Columbia":
            self.cityInput["values"] = (' Greater Vancouver Area', ' Kelowna', ' Nanaimo', ' Victoria',' Whistler' )
        elif self.provinceInput.get().strip() == "Manitoba":
            self.cityInput["values"] = ( ' Winnipeg' )
        elif self.provinceInput.get().strip() == "Nova Scotia":
            self.cityInput["values"] = (' Halifax')
        elif self.provinceInput.get().strip() == "Ontario":
            self.cityInput["values"] = (' Barrie', ' Hamilton', ' Kitchener Area',' Ottawa / Gatineau Area',' Toronto (GTA)' )
        elif self.provinceInput.get().strip() == "Qu\u00e9bec":
            self.cityInput["values"] = (' Greater Montr\u00e9al',' Qu\u00e9bec City')
        elif self.provinceInput.get().strip() == "Saskatchewan":
            self.cityInput["values"] = (' Regina Area')


    #Function to confirm location and input in table
    def ConfirmLocation(self, event):
        prv = self.provinceInput.get().strip()
        cty = self.cityInput.get().strip()
        check = (prv, cty)
        msg = " You selected {} as Province and {} as City Location for search, Are You Sure ?".format(prv, cty)
        if check not in self.locations:
            self.answer = messagebox.askquestion("Confirm Location", msg)
         
            if self.answer.strip() == "yes":
                self.locations.append(check)
                self.count += 1
                loc = (self.count, prv, cty)   
                # adding data to the treeview
                self.tbl.insert('', tk.END, values=loc)
            else :
                pass
        else :
            messagebox.showerror("Error", "Location Already Selected")


    #Function to remove a record on double click
    def removeRecord(self, event):
        item = self.tbl.selection()
        remianing = []
        if len(item) != 0:
            selected_item = item[0]
            cnt = 0
            start = False
            for i in self.tbl.get_children():

                if i ==  selected_item :
                    item = self.tbl.item(i)
                    start = True
                    print(item["values"][0])
                    cnt = item["values"][0] - 1
                    print(cnt)
                    continue
                    
                
                if start:
                    item = self.tbl.item(i)
                    cnt += 1
                    loc = (cnt, item["values"][1], item["values"][2])
                    print(loc)
                    remianing.append(loc)
                    self.tbl.delete(i)

            self.count = cnt
            self.tbl.delete(selected_item)

            for loc in remianing:
                # print(loc)
                self.tbl.insert('', tk.END, values=loc)

                
        # print("you clicked on", self.tbl.item(item,"text"))


    #Function to clear table data
    def clearRecords(self):
        for i in self.tbl.get_children():
            print(i)
            self.tbl.delete(i)
        self.count = 0










if __name__ == "__main__":
    ws  = kijijiApp()
    # ws.window_loop()

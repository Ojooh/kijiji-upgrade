import json 
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image  
# import subprocess
# import threading
# from selenium.common.exceptions import TimeoutException, WebDriverException
LARGEFONT =("Verdana", 35)
PATHS = {"logo" : "img/kijiji.png", "startBtn" : "img/startBtn.png", "searchBtn" : "img/searchBtn.jpg"}


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
        #Labels, bottoms and Entry of Information
        imgLogo = ImageTk.PhotoImage(Image.open(PATHS["logo"]).resize((65, 65)))
        labelLogo = ttk.Label(self, image=imgLogo, background="#0D0C52")
        labelLogo.image = imgLogo
        labelLogo.place(x = 230, y = 0)
        labelLogo.image = imgLogo        
        
        titleHead = ttk.Label(self, background="#0D0C52", text ="KIJIJI AUTOBOT", font=("Roboto Condensed", 20, "bold"), foreground = "#FFFFFF")
        titleHead.place(x = 300, y = 15)

        labelKey = ttk.Label(self, text ="Keyword:", font=("Roboto Condensed", 13, "bold"), background="#0D0C52", foreground = "royalblue")
        labelKey.place(x = 345, y = 75)        

        inputKeyword = Entry(self, width=65, justify="center", font=("Roboto Condensed", 13))
        inputKeyword.place(x = 80, y = 110)

        labelInfo = ttk.Label(self, text ="Please separate multiple keywords with a comma", font=("Roboto Condensed", 13), background="#0D0C52", foreground = "white")
        labelInfo.place(x = 200, y = 150)

        labelProvice = ttk.Label(self, text = "Province:", font=("Roboto Condensed", 17), background="#0D0C52", foreground = "white")
        labelProvice.place(x=180, y=190)

        labelCity = ttk.Label(self, text = "City:", font=("Roboto Condensed", 17), background="#0D0C52", foreground = "white")
        labelCity.place(x=490, y=190)

        inputProvince = Entry(self, width=25, justify="center", font=("Roboto Condensed", 13))
        inputProvince.place(x = 80, y = 230)
        
        inputCity = Entry(self, width=25, justify="center", font=("Roboto Condensed", 13))
        inputCity.place( x=445, y=230)
        
        labelColor = Label(self, width=84, height=17, background="white")
        labelColor.place(x=80, y=270)

        labelProvice2 = ttk.Label(self, width=24, text = "                Province:", font=("Roboto Condensed", 16), background="lightgray", foreground = "black" )
        labelProvice2.place(x = 80, y = 270)

        labelCity2 = ttk.Label(self, width=24, text = "                   City:", font=("Roboto Condensed", 16), background="lightgray", foreground = "black" )
        labelCity2.place(x = 380, y = 270)

        labelText = Label(self, width=41, height=15, background="lightgray")
        labelText.place(x=80, y=302)

        labelText2 = Label(self, width=41, height=15, background="lightgray")
        labelText2.place(x=380, y=302)

        buttomClear = Button(self, text="CLEAR ALL RECORDS", relief='flat', bg="navy", font=("Roboto Condensed", 14, "bold"), foreground="white", overrelief="flat")
        buttomClear.place(x=250, y=550)

        imgSearch = ImageTk.PhotoImage(Image.open(PATHS["searchBtn"]).resize((175, 45)))
        buttonSearch = Button(self, image=imgSearch, relief='flat', bg='#0D0C52')
        buttonSearch.image = imgSearch
        buttonSearch.place(x=285, y=600)
        buttonSearch.image = imgSearch

  
        

if __name__ == "__main__":
    ws  = kijijiApp()
    # ws.window_loop()

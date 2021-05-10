import json 
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image  
# import subprocess
# import threading
# from selenium.common.exceptions import TimeoutException, WebDriverException
LARGEFONT =("Verdana", 35)
PATHS = {"logo" : "img/kijiji.png", "startBtn" : "img/startBtn.png"}


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
        label = ttk.Label(self, text ="Form Page", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        

if __name__ == "__main__":
    ws  = kijijiApp()
    # ws.window_loop()

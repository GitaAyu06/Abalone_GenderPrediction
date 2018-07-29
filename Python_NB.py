#libraries
import xlsxwriter
import tkinter as tk
from tkinter import *
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import time
from collections import Counter as ct
from tkinter.messagebox import showinfo as si
from tkinter.messagebox import showwarning as sw

#import matplotlib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#machine learning libraries : sklearn
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

root = Tk()

#Functional Command

def program_quit():
    root.destroy()

def help_f():
    si("HELP","1.Start this program by select Execute on menus. \n2.Enter your file name (e.g = Test.csv). \n3.The naive bayes output file will be printed in xlsx \n4.Choose yes if you want to show the Pie Chart. \nNotes : \n- Output file name = \'Output.xlsx\' \n- File location is in the same folder of the program")

def func_p():
    x = 1
    file_name = sd.askstring("File Name","Enter your file name ")
    data = pd.read_csv(file_name)
    while x == 1 :
        if file_name is not None :
            x = 0
            si("","File Loaded!")

            #mapping data
            data["Sex_cleaned"]=np.where(data["Sex"]=="M","Male",
                                         (np.where(data["Sex"]=="F","Female","Infant")))
            data=data[[
                "Sex_cleaned",
                "Length",
                "Diameter",
                "Height",
                "Whole weight",
                "Shucked weight",
                "Viscera weight",
                "Shell weight",
                "Rings"
                ]].dropna(axis=0, how='any')

            #Split dataset
            train, test = train_test_split(data, test_size=0.6, random_state=int(4))
            gnb = GaussianNB()
            indicators =[
                "Length",
                "Diameter",
                "Height",
                "Whole weight",
                "Shucked weight",
                "Viscera weight",
                "Shell weight",
                "Rings"
                ]
            gnb.fit(train[indicators].values, train["Sex_cleaned"])
            y_pred = gnb.predict(test[indicators])
        
            #Print Performance Indicator
            data_accuracy = ("Total data {} points : {}, Accuracy {:05.2f}%"
                  .format(
                      test.shape[0],
                      (test["Sex_cleaned"] != y_pred).sum(),
                      100*(1-(test["Sex_cleaned"] != y_pred).sum()/test.shape[0])
                      ))
            test_data = pd.concat([test[indicators], test["Sex_cleaned"]], axis=1)
            test_data["Sex Prediction"] = y_pred
            test_data["Data Accuracy"] = data_accuracy

            #Excel Writer
            writer = pd.ExcelWriter('Output.xlsx', engine = 'xlsxwriter')
            test_data.to_excel(writer,sheet_name='Sheet1')
            writer.save()
            si("","Output Created! Check it out!")
            answer = mb.askyesno("Question","Do you want to check the Data Chart?")
            if answer==True :
                #Counter
                counts = ct(y_pred)
                count_Male = counts['Male']
                count_Female = counts['Female']
                count_Infant = counts['Infant']
                slices = [count_Male,count_Female,count_Infant]
                cols = ['#00ffc3','#ff00cb','#ffd000']
                #Pie Chart
                fig = Figure(figsize=(100,100))
                a = fig.add_subplot(111)
                a.pie(slices, labels=['Male','Female','Infant'], colors = cols, shadow = True, startangle = 90,autopct='%1.1f%%')
                a.legend()
                canvas = FigureCanvasTkAgg(fig)
                canvas.get_tk_widget().pack(fill=BOTH,expand=True)
                return fig
                FigureCanvasTk.draw()
            else :
                root.destroy()
    else :
        sw("Warning", "Please re - enter your input")
        

#Creating Main Window
class Window(Frame):
    def client_exit(self):
        exit()

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("PyNB v1.0")
        self.pack(fill=BOTH, expand = 1)
        
        sw("WARNING!!!","Make sure your input file is in the same folder with the program or it will lead an error!!!".upper())

        menu = Menu(self.master)
        self.master.config(menu=menu)
        load = Image.open('cover.jpg')
        render = ImageTk.PhotoImage(load)
        img = Label(image=render)
        img.image = render
        img.place(x=0,y=0)
        #add menu cascade
        menu.add_cascade(label='Help', command = help_f)
        menu.add_cascade(label='Execute', command = func_p)
        menu.add_cascade(label='Quit',command = program_quit)


root.geometry("400x200")
app = Window(root)
root.mainloop()

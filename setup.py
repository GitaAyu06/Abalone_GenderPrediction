import os
os.environ['TCL_LIBRARY'] = r'C:\Users\Asus\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Asus\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'
from cx_Freeze import setup, Executable

setup(name='PyNB',version='0.5',description='Implementation of Naive Bayes Algorithm for predicting Abalone Gender',executables = [Executable("Python_NB.py")])

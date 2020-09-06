
import tkinter as tk
from tkinter import messagebox as mb
import cvtest
import audiotest

def fbbutton():
    result = cvtest.facerec()
    if result > 0.3:
        mb.showwarning('Warning', 'Our Test Indicates that you may be showing symptoms of Stroke')


def abbutton():
    result = audiotest.speechtest()
    if result:
        mb.showwarning('Warning', 'Our Test Indicates that you may be showing symptoms of Stroke')

def lbbutton():
    result = cvtest.armrec()
    if result > 300:
        mb.showwarning('Warning', 'Our Test Indicates that you may be showing symptoms of Stroke')


top = tk.Tk()
fb = tk.Button(top, text="face recognition", command=fbbutton)
fb.pack()
lb = tk.Button(top, text="Arm Strength Test(UNSTABLE)", command=lbbutton)
lb.pack()
ab = tk.Button(top, text="audio recognition", command=abbutton)
ab.pack()

top.mainloop()
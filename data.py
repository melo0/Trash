#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Program do obliczania liczby dni/tygodni/miesięcy od wpisanej daty do dnia dzisiejszego (lub wprowadzonej ręcznie daty)


import tkinter.ttk
from tkinter import * 
import time
import datetime


def oblicz():
    pole_t3.delete(1.0, END)
    pole_t4.delete(1.0, END)
    pole_t5.delete(1.0, END)
    data1 = datetime.datetime.strptime(pole_t1.get(), "%Y-%m-%d").date()
    data2 = datetime.datetime.strptime(pole_t2.get(), "%Y-%m-%d").date()
    data3 = str(data2 - data1)
    pozycja = data3.index("days")
    pole_t3.insert(END, int(data3[0:pozycja-1]))
    pole_t4.insert(END, (int(data3[0:pozycja-1])/7))
    pole_t5.insert(END, int(data3[0:pozycja-1])/30.4)


okno = tkinter.Tk()
okno.title("Data")
okno.geometry("300x150")


pole_t1 = tkinter.Entry(okno)
pole_t2 = tkinter.Entry(okno)
pole_t3 = tkinter.Text(height = 1, width = 20)
pole_t4 = tkinter.Text(height = 1, width = 20)
pole_t5 = tkinter.Text(height = 1, width = 20)

pole_t1.insert(END, "2016-12-16")
pole_t2.insert(END, time.strftime("%Y-%m-%d"))


etykieta1 = tkinter.Label(okno, text = "Data początkowa: ")
etykieta2 = tkinter.Label(okno, text = "Dzisiejsza data: ")
etykieta3 = tkinter.Label(okno, text = "Liczba dni: ")
etykieta4 = tkinter.Label(okno, text = "Liczba tygodni: ")
etykieta5 = tkinter.Label(okno, text = "Liczba miesięcy: ")



pole_t1.grid(row=0, column = 2)
pole_t2.grid(row=2, column = 2)
pole_t3.grid(row=4, column = 2)
pole_t4.grid(row=6, column = 2)
pole_t5.grid(row=8, column = 2)

etykieta1.grid(row=0, column = 1)
etykieta2.grid(row=2, column = 1)
etykieta3.grid(row=4, column = 1)
etykieta4.grid(row=6, column = 1)
etykieta5.grid(row=8, column = 1)

przycisk = tkinter.Button(okno, text = "Oblicz", command = lambda: oblicz() )
przycisk.grid(row = 11, column = 2)

okno.mainloop() 

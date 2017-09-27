#! python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import openpyxl, pprint
import win32com.client as win32


def do_pliku(dane):
    plik = open("dane.txt", "w")
    plik.write(dane)
    plik.close()
    return

def emailer(text, subject, recipient):

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    mail.HtmlBody = text
    attachment = str(r'C:\Users\lsnopek\workspace\All_Programs\dane.txt')
    mail.Attachments.Add(attachment)
    mail.send

Plik = openpyxl.load_workbook('test.xlsx')
Arkusz = Plik.get_sheet_by_name('Arkusz1')
baza = {}
msg =  "Data zał.,Flow,Ferma zał.,SMR,numer,fermy,Godz.Zał.,Rodzaj zwierząt,Liczba zwierząt,Ferma docelowa,SMR,numer fermy,Powiat,km,godz. Rozł.,pojazd,nr rej pojazdu,nr rej naczepy/przyczepy,Uwagi" + "\n"


for wiersz in range(2, Arkusz.max_row):
    tresc = []
    for c in Arkusz['A'+str(wiersz):'Q'+str(wiersz)]:
        for v in c:
            tresc.append(v.value)
    adres = Arkusz['T' + str(wiersz)].value
    baza.setdefault(adres,{'zawartość': []})
    baza[adres]['zawartość'] += [tresc]

for i in baza:
    for k in baza[i]['zawartość']:
        msg += "\n" + str(k)
        do_pliku(msg)
    emailer('W załączniku znajdują się dane z transportów - TESTY', 'TEST - Wysłki danych', i)
    msg = "Data zał.,Flow,Ferma zał.,SMR,numer,fermy,Godz.Zał.,Rodzaj zwierząt,Liczba zwierząt,Ferma docelowa,SMR,numer fermy,Powiat,km,godz. Rozł.,pojazd,nr rej pojazdu,nr rej naczepy/przyczepy,Uwagi" + "\n"

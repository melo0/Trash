#! python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import openpyxl, pprint
import smtplib

print('Opening workbook...')
wb = openpyxl.load_workbook('test.xlsx')
sheet = wb.get_sheet_by_name('Arkusz1')
baza = {}
nadawca = " "
haslo = " "

server = smtplib.SMTP("smtp.poczta.onet.pl", 587)
server.starttls()
server.login(nadawca, haslo)



#server.set_debuglevel(1)
msg = []

print('Reading rows...')

for row in range(2, sheet.max_row):
    tresc = []
    tresc.append(str(sheet['A'+ str(row)].value))
    tresc.append(str(sheet['B'+ str(row)].value))
    tresc.append(str(sheet['C'+ str(row)].value))
    tresc.append(str(sheet['D'+ str(row)].value))
    tresc.append(str(sheet['E'+ str(row)].value))
    tresc.append(str(sheet['F'+ str(row)].value))
    tresc.append(str(sheet['G'+ str(row)].value))
    tresc.append(str(sheet['H'+ str(row)].value))
    tresc.append(str(sheet['I'+ str(row)].value))
    tresc.append(str(sheet['J'+ str(row)].value))
    tresc.append(str(sheet['K'+ str(row)].value))
    tresc.append(str(sheet['L'+ str(row)].value))
    tresc.append(str(sheet['M'+ str(row)].value))
    tresc.append(str(sheet['N'+ str(row)].value))
    tresc.append(str(sheet['O'+ str(row)].value))
    tresc.append(str(sheet['P'+ str(row)].value))
    tresc.append(str(sheet['Q'+ str(row)].value))
    tresc.append(str(sheet['R'+ str(row)].value))
    adres = sheet['T' + str(row)].value
    baza.setdefault(adres,{'zawartość': []})
    baza[adres]['zawartość'] += [tresc]

for i in baza:
    print('adres do wysyłki: ' + i)

    for k in baza[i]['zawartość']:
        msg += [k]
    print(msg)

    # server.sendmail('test_rozsylania@agriplus.pl', i, msg)
    msg = []

server.quit()

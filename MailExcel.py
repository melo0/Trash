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

for wiersz in range(2, Arkusz.max_row):
    tresc = []
    for c in Arkusz['A'+str(wiersz):'Q'+str(wiersz)]:
        for v in c:
            tresc.append(v.value)
    adres = Arkusz['T' + str(wiersz)].value
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

#! python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------
# Version 2.02
#--------------

import win32com.client as win32
import pyexcel, xlsxwriter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.ttk
import string, os
import time
import pyodbc
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def To_excel(value):
    workbook = xlsxwriter.Workbook('ZamBiezacyTydz.xlsx')
    worksheet = workbook.add_worksheet('Nowy')
    title = workbook.add_format(({'border': 1, 'border_color': '#000000', 'bold' : True}))
    string_format = workbook.add_format(({'border': 1, 'border_color': '#000000'}))
    data_format = workbook.add_format({'num_format': 'dd-mm-yyyy','border': 1, 'border_color': '#000000'})
    rd = 0
    cd = 0
    worksheet.set_column(0, 1, 12)
    worksheet.set_column(2, 2, 45)
    worksheet.set_column(3, 3, 15)
    worksheet.set_column(4, 4, 10)
    worksheet.set_column(5, 5, 8)
    worksheet.set_column(6, 6, 30)
    worksheet.set_column(7, 7, 13)
    worksheet.set_column(8, 8, 40)
    worksheet.set_column(9, 9, 7)
    worksheet.set_column(10, 11, 18)
    worksheet.set_column(12, 12, 30)
    worksheet.set_column(13, 13, 28)
    worksheet.set_column(14, 14, 10)
    worksheet.set_column(15, 15, 40)
    worksheet.set_column(16, 16, 9)
    worksheet.set_column(17, 17, 30)
    worksheet.set_column(18, 18, 7)
    worksheet.set_column(19, 19, 31)
    print(value)
    for i in value:
        for k in i:
            if rd == 0:
                worksheet.write(rd, cd, k, title)
            else:
                if (cd ==10 or cd == 11):
                    worksheet.write(rd, cd, k, data_format)
                else:
                    worksheet.write(rd, cd, k, string_format)
            cd += 1
        rd += 1
        cd = 0
    worksheet.autofilter(0 , 1, 0, 19)
    workbook.close()

def Emailer(text, subject, recipient):
    server = smtplib.SMTP('mail_server_address', 25) # mail server address
    fileToSend = 'ZamBiezacyTydz.xlsx'
    emailfrom = 'SystemPowiadomien@animex.pl'
    message = MIMEMultipart()
    message['From'] = emailfrom
    message['To'] = recipient
    message['Subject'] = subject
    message.preamble = subject
    wiadomosc = MIMEText(text, 'plain')
    message.attach(wiadomosc)
    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    if maintype == "text":
        print
        'text'
        fp = open(fileToSend)
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    else:
        print
        'else'
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    message.attach(attachment)
    server.sendmail(emailfrom, recipient, message.as_string())
    server.quit()


def Connection(sql):
    conn = pyodbc.connect('DSN=DSN_name;UID=USER_name;PWD=Secret_Password') #MS SQL connection data
    cursor = conn.cursor()
    cursor.execute(sql)
    table = cursor.fetchall()
    return table


def Processing():
    new_table = []
    sql = ("""\
        SELECT DISTINCT 
    	  (case 
    	  when p1.[order_type] = 'K' then 'Komercja'
    	  when p1.[farm] like '%D' then 'DRÓB' 
    	  else 'Trzoda' end) as 'RODZAJ ZAMOWIENIA'
    	  ,(case 
    	  when p1.[farm]='' then p1.customer_2
    	  else p1.[farm] end) as 'FERMA/ODBIORCA'
    	  ,(case
    	  when p1.[farm]='' then p9.description 
    	  else p3.location end) as 'NazwaFermy/Odbiorca'
          ,(case
    	  when p1.[lot]='' then '-'
    	  else p1.[lot] end) as 'LOT'
    	  , (Case 
    	  When p1.[order_type] = 'K' then '-'
    	  when p1.[farm] like '%D' then '-'
    	  When p7.[status_af]=1 Then 'Never Ever' 
    	  When p7.[status_af]=2 Then 'Clasic' 
    	  Else 'Not AF' End) as 'Status AF'
          ,(case 
    	  when p1.customer_1='' then '-'
    	  else p1.customer_1 end) as 'Płatnik'
    	  ,(case 
    	  when p1.customer_1='' then '-'
    	  else p9.description end)as 'Płatnik' 
    	  ,p4.[material] as 'NR MATERIALU'
          ,p4.[name] as 'MATERIAL'
    	  ,p1.[quantity] as 'ILOSC'
    	  ,p1.[day_order] as 'DATA ZAMOWIENIA'
          ,p1.[day_delivery] as 'DATA DOSTARCZENIA'
          ,p5.[name] as 'WYTWORNIA'
          ,p2.[name] as 'OSOBA WPROWADZAJACA ZAM'
          ,p3.[servman] as 'SVM FERMY'
    	  ,(case 
    	  when cast((p1.[status]) as char(2)) = '10' then 'Oczekuje u Logistyka'
    	  when cast((p1.[status]) as char(2)) = '9' then 'Oczekuje na koordynatora \ komercja w BOK'
    	  when cast((p1.[status]) as char(2)) = '19' then 'Blad'
    	  when cast((p1.[status]) as char(2)) = '40' then 'OK'
    	  when cast((p1.[status]) as char(2)) = '41' then 'Zaksiegowane - komercja'
    	  when cast((p1.[status]) as char(2)) = '45' then 'OK'
    	  when cast((p1.[status]) as char(2)) = '20' then 'OK'
    	  when cast((p1.[status]) as char(2)) = '30' then 'Anulowane'
    	  else cast((p1.[status]) as char(2)) end) as 'STATUS'
    	  ,p1.[flow] as 'FLOW NR' 
    	  ,p6.[location] as 'FLOW NAZWA'
    	  ,p1.[id]
    	  ,p2.[email]
      FROM [ServiceManProd].[dbo].[registry_fodder] p1
      left outer join [ServiceManProd].[dbo].[shadow_user] p2 on
      p1.[identity] = p2.[id]
      left outer join [ServiceManProd].[dbo].[registry_farm] p3 on
      p1.[farm] = p3.[sap]
      left outer join [ServiceManProd].[dbo].[registry_material] p4 on
      p1.[material] = p4.[material]
      left outer join [ServiceManProd].[dbo].[registry_supplier] p5 on
      p1.[supplier] = p5.[supplier]
      left outer join [ServiceManProd].[dbo].[registry_farm] p6 on
      p1.[flow] = p6.[sap]
      left join [ServiceManProd].[dbo].[registry_lot] p7 on 
      p1.[lot] = p7.[lot]
      left outer join [ServiceManProd].[dbo].[registry_customer] p8 on
      p1.[customer_1] = p8.[number]
      left outer join [ServiceManProd].[dbo].[registry_customer] p9 on
      p1.[customer_2] = p9.[number]
      Where 

      p1.[day_delivery] between 
      	DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 0)
    and
    	DATEADD(wk, DATEDIFF(wk,0,GETDATE()), 6)
      and p1.[ancestor] is null
      order by [RODZAJ ZAMOWIENIA], [DATA DOSTARCZENIA] DESC
      """)
    table = Connection(sql)
    dictionary = {}
    new_table.append(('RODZAJ ZAMOWIENIA', 'FERMA/ODBIORCA', 'NazwaFermy/Odbiorca', 'LOT', 'Status AF', 'Płatnik', 'Płatnik', 'NR MATERIALU', 'MATERIAL', 'ILOSC', 'DATA ZAMOWIENIA', 'DATA DOSTARCZENIA', 'WYTWORNIA', 'OSOBA WPROWADZAJACA ZAM', 'SVM FERMY', 'STATUS', 'FLOW NR', 'FLOW NAZWA', 'id', 'email'))
    for row in table:
        dest1 = str(row[19])
        Values = row[:20]
        if '@' in dest1:
            dictionary.setdefault(dest1, [])
        if '@' in dest1:
            dictionary[dest1] += [Values]
    return dictionary , new_table


def Send():
    dictionary, new_table = Processing()
    for cel in dictionary:
        x = new_table + dictionary[cel]
        To_excel(x)
        Emailer(('TEST - Zamowienia pasz biezacy tydzien Stan na '+ time.strftime("%Y-%m-%d", time.localtime())), ('TEST - Zamowienia pasz serviceman biezacy tydzien z dnia '+time.strftime("%Y-%m-%d", time.localtime())), cel)
        print(cel)
    if os.path.isfile('ZamBiezacyTydz.xlsx'):
        os.unlink('ZamBiezacyTydz.xlsx')


if __name__ == "__main__":
    Send()








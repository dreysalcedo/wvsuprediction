# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 18:51:27 2021

@author: gtxnn
"""

import mysql.connector

db = mysql.connector.connect(
     host = "sdffea.com",
    user = "ezpaydbadmin",
    password = "WvsuCictThesis2020",
    database = "ezpaydb"     
    )
cursor = db.cursor()


def InsertBlob(FilePath):
    with open(FilePath, "rb") as File:
        BinaryData = File.read()
    SQLStatement = "INSERT INTO currentprediction(image)VALUES(%s)" 
    cursor.execute(SQLStatement, (BinaryData, ))
    db.commit()

def RetrieveBlob(id):
     SQLStatement2 = "SELECT * FROM currentprediction WHERE id = '{0}'"
     cursor.execute(SQLStatement2.format(str(id)))
     MyResult = cursor.fetchone()[1]
     StoreFilePath = "static/uploads/img{0}.jpg".format(str(id))
     print(MyResult)
     with open(StoreFilePath, "wb") as File:
         File.write(MyResult)
         File.close()
print("1. insert image\n2. read image" )
MenuInput = input()
if int(MenuInput) == 1:
    UserFilePath = input("Enter File Path:")
    InsertBlob(UserFilePath)
elif int(MenuInput) == 2:
    UserIDchoice= input("Enter id: ")
    RetrieveBlob(UserIDchoice)
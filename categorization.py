import pandas as pd
import mysql.connector
def categorization(table_name,nummer=1):
    myDB = mysql.connector.connect(host='localhost',
                                   user='root', passwd='Yuceisa@jaruselam0000', port='3306',
                                   database='deux')
    mycursor = myDB.cursor()
    mycursor.execute(f"SELECT Symbol, Rsi5th,Rsi4th,Rsi3th,Rsi2th,Rsi1th FROM {table_name}\n")
    myresult = mycursor.fetchall()
    try:
        for x in range(len(myresult)):
            Rsi5th = float(myresult[x][1])
            Rsi4th = float(myresult[x][2])
            Rsi3th = float(myresult[x][3])
            Rsi2th = float(myresult[x][4])
            Rsi1th = float(myresult[x][5])
            Color = []
            if Rsi5th >= 70:
                Color.append("P")
            elif 55 <= Rsi5th < 70:
                Color.append("B")
            elif 45 <= Rsi5th < 55:
                Color.append("U")
            elif 40 <= Rsi5th < 45:
                Color.append("R")
            elif Rsi5th < 40:
                Color.append("X")

            if Rsi4th >= 70:
                Color.append("P")
            elif 55 <= Rsi4th < 70:
                Color.append("B")
            elif 45 <= Rsi4th < 55:
                Color.append("U")
            elif 40 <= Rsi4th < 45:
                Color.append("R")
            elif Rsi4th < 40:
                Color.append("X")

            if Rsi3th >= 70:
                Color.append("P")
            elif 55 <= Rsi3th < 70:
                Color.append("B")
            elif 45 <= Rsi3th < 55:
                Color.append("U")
            elif 40 <= Rsi3th < 45:
                Color.append("R")
            elif Rsi3th < 40:
                Color.append("X")

            if Rsi2th >= 70:
                Color.append("P")
            elif 55 <= Rsi2th < 70:
                Color.append("B")
            elif 45 <= Rsi2th < 55:
                Color.append("U")
            elif 40 <= Rsi2th < 45:
                Color.append("R")
            elif Rsi2th < 40:
                Color.append("X")



            if Rsi1th >= 70:
                Color.append("P")
            elif 55 <= Rsi1th < 70:
                Color.append("B")
            elif 45 <= Rsi1th < 55:
                Color.append("U")
            elif 40<= Rsi1th < 45:
                Color.append("R")
            elif Rsi1th < 40:
                Color.append("X")

            try:
                if Color[4] == "B" or Color[4] == "U":
                    if Color[3] == "U":
                        if Color[2] == "U" :
                            if Color[1] == "U" or Color[1] == "R":
                                if Color[0] == "R":

                                    print(nummer, myresult[x][0], Color)
                                    nummer += 1
            except:
                pass



    except Exception as e:
        print(f"An error occurred: {e}")

categorization("nasdaq_stocks")

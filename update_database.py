import mysql.connector
import yfinance as yf
#update all columns
def update_columns(table_name):
    myDB = mysql.connector.connect(host='localhost',
                                   user='root', passwd='Yuceisa@jaruselam0000', port='3306',
                                   database='deux')
    mycursor = myDB.cursor()
    for i in range(10, 1, -1):
        mycursor.execute(f"UPDATE {table_name}\n"
                         f"SET Price{i}th = Price{i - 1}th,Rsi{i}th = Rsi{i - 1}th\n")
    myDB.commit()
    mycursor.close()
    myDB.close()
def new_rsi(table_name,name_of_the_stock):
    myDB = mysql.connector.connect(host='localhost',
                                   user='root', passwd='Yuceisa@jaruselam0000', port='3306',
                                   database='deux')
    mycursor = myDB.cursor()
    mycursor.execute(f"SELECT Price1th,AG,AL FROM {table_name}\n"
                     f"WHERE Symbol = '{name_of_the_stock}'")
    myresult = mycursor.fetchall()
    latest_price = yf.Ticker(name_of_the_stock).history(period="1d").iloc[0]["Close"]
    diff = latest_price-float(myresult[0][0])
    if (diff) > 0:
        new_AG = round((diff+13*float(myresult[0][1]))/14,8)
        new_AL = round((float((13*myresult[0][2])/14)),8)
        print(new_AG,new_AL)
    else:
        new_AG = round((float((13*myresult[0][1])/14)),8)
        new_AL = round((abs(diff)+13*float(myresult[0][2]))/14,8)
        print(new_AG,new_AL)
    new_rsi = 100-(100/(1+(new_AG/new_AL)))
    print(new_rsi,100-(100/(1+new_AG/new_AL)))
    list = [latest_price, new_rsi, new_AG,new_AL]
    return list

#use when daily update needed
def update_the_databse(table_name):
    '''
    new_values_list = =[last_days_price,last_days_rsi,new_AG,new_AL]
    '''
    update_columns(table_name)
    myDB = mysql.connector.connect(host='localhost',
                                   user='root', passwd='Yuceisa@jaruselam0000', port='3306',
                                   database='deux')
    mycursor = myDB.cursor()
    mycursor.execute(f"SELECT Symbol FROM {table_name}\n")
    myresult = mycursor.fetchall()
    for name in myresult:
        try:
            new_values_list = new_rsi(table_name, name[0])
            mycursor.execute(f"UPDATE {table_name}\n"
                         f"SET Price1th = {new_values_list[0]},Rsi1th = {new_values_list[1]},AG = {new_values_list[2]},AL = {new_values_list[3]}\n"
                         f"WHERE Symbol = '{name[0]}'")
        except Exception as e:
            print(f"An error occurred while updating {name[0]}: {e}")
    myDB.commit()
    mycursor.close()
    myDB.close()
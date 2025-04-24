from initial_data_extractor import *
from update_database import *

print("What opeation would you like to do?\nFilling a new database (f) or Updating a database (u)? ")
the_decleration = input()
if the_decleration == "f":
    ''' This function is runned if there is no database for your rsi and price values. 
    it creates a database using google sheets api in a mysql database
    it stores the closed prices database thus must be runned after the market is closed'''
    filling_row("nasdaqnames.csv","nasdaq_stocks")
elif the_decleration == "u":
    ''' This function is runned if there is a database for your rsi and price values.
    it updates the values in the database. 
    !!! IT MUST BE RUNNED AFTER THE STOCK MARKET IS CLOSED'''
    update_the_databse("nasdaq_stocks")
else:
    "a problem has occured"
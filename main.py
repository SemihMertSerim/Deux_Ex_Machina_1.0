from initial_data_extractor import *
from update_database import *

print("What opeation would you like to do?\nFilling a new database (f) or Updating a database (u)? ")
the_decleration = input()
if the_decleration == "f":
    filling_row("nasdaqnames.csv","nasdaq_stocks")
elif the_decleration == "u":
    update_the_databse("nasdaq_stocks")
else:
    "a problem has occured"
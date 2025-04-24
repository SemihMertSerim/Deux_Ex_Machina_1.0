Hi visitor, this is the readme.txt for the curious eyes

Explanation of each file and each function:

Categorization: It consist of 1 main function to filter stocks according to the last 5 days rsi values and can be manually change

creddentials.json: It is necesarry to access google api. There are items hided to keep my accounts safe. If you want to
download and try this software you must acquire your own credentials. through google console you can download exact same
file and change with it.

google_sheets_IDs.csv: It is a csv file which holds the IDs of required spreadsheets to fill and update mysql

initial_data_extractor.py: it fetchs the stock markets last 200 days data to calculate rsi and required other parameters
(Average Gain and Average Loss is required for rsi calculation).
It is important to allow required permissions for google sheets api and you need at least 1500 writing per minute request
to prevent run time errors. Google allows your request at most 1-1.5 business day. You have to have mysql workbench downloaded
and created the required database and table

main.py: Here is where you decide you will update the database or fill a new database. With version 1.0.0 there is no
time based update you have to have it manually and no visual interpreter.

nasdaqnames.csv: Here is where the software holds the names of the stocks to fill a database or update it. there is no auto
remove system for a delisted stock it must be done manually

update_database.py: This is the most used function for a everyday user. It updates the data and keeps your database fresh.
You must be carefull not to miss a day without updating, there is no auto update system as for version 1.0.0. Also you
have to have correct versions of yfinance, google api, mysql workbench.
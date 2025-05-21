Hi visitor, this is the readme.txt for the curious eyes

Explanation of each file and each function:

Categorization: It consists of 1 main function to filter stocks according to the last 5 days RSI values and can be manually changed

credentials.json: It is necessary to access the google api. There are items hidden to keep my accounts safe. If you want to
download and try this software, you must acquire your own credentials. Through Google Console, you can download the same
file.

google_sheets_IDs.csv: It is a CSV file that holds the IDs of required spreadsheets to fill and update MySQL

initial_data_extractor.py: it fetches the stock market's last 200 days data to calculate RSI and required other parameters
(Average Gain and Average Loss are required for RSI calculation.)
It is important to allow required permissions for the Google Sheets API, and you need at least 1500 writing per minute requests
to prevent runtime errors. Google approves your request at most 1-1.5 business days. You have to have MySQL Workbench downloaded
and create the required database and table

main.py: Here is where you decide whether you will update the database or fill a new database. With version 1.0.0, there is no
time-based update, you have to do it manually, and no visual representation for 1.0.0.

nasdaqnames.csv: Here is where the software holds the names of the stocks to fill a database or update it. There is no auto
remove for delisted stocks, it must be done manually

update_database.py: This is the most used function for an everyday user. It updates the data and keeps your database fresh.
You must be careful not to miss a day without updating, there is no auto update system as for version 1.0.0. Also you
have to have correct versions of yfinance, google api, MySQL Workbench.

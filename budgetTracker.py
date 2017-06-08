from __future__ import print_function
from appJar import gui
import sqlite3
import datetime
#GLOBAL VARIABLES
global sqlite_file, total_amount, date_time,description,message_board, cash_flow
sqlite_file =  'budgetTracker.sqlite'
total_amount = 0
date_time = " "
description = " "
message_board = " "
csh_flow = 0
#class used for creating table if no table exists
class BtDatabase():
    """
    input: none
    output: If database already exists, will promt user that database exists
    If database does not exists, will create database for the application
    """
    #defining the database file
    global sqlite_file,message_board,total_amount
    def __init__(self):
        self.sql = ('CREATE TABLE transactions(ID INTEGER PRIMARY KEY,date_time TEXT, amount REAL, category TEXT, description TEXT, account_total  REAL)')

    #checks whether or not database exists, and grabs total from it if not then creates a new one
    def create_db(self):
        try:
            open(sqlite_file)
            message_board = "-Database already exists- "
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute('SELECT SUM(amount) FROM transactions')
            global total_amount
            total_amount = truncate(c.fetchone()[0],2)

            return message_board
        except:
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute(self.sql)
            conn.commit()
            sql = ('INSERT INTO transactions(ID,amount,category,description,account_total) VALUES(0,0,"Begingin entry"," ",0)')
            c.execute(sql)
            conn.commit()
            conn.close()
            message_board = "-Database created successfully- "
            return message_board

class Update_Database():

    #set global variables
    global sqlite_file,total_amount,message_board

    def __init__(self, data_entries):

        self.data_entries = data_entries


    def update(self):
        try:
            open(sqlite_file)
            conn = sqlite3.connect(sqlite_file)
            c =conn.cursor()
            sql = (
            'INSERT INTO transactions(date_time,amount,category,description,account_total)VALUES(?,?,?,?,0)')
            c.execute(sql, self.data_entries)
            conn.commit()
            cur_Pos = c.lastrowid
            c.execute('SELECT SUM(amount) FROM transactions')
            global total_amount
            total_amount = truncate(c.fetchone()[0],2)
            sql = ('UPDATE transactions set account_total = {tot} WHERE ID = {cp}'.format(tot=total_amount,cp=cur_Pos))
            c.execute(sql)
            conn.commit()
            conn.close()
            message_board = "-Database updated successfully- "
            return message_board
        except:
            message_board = "-Database could not be updated- "
            return message_board

class CashFlow():
    global sqlite_file, message_board, csh_flow
    def __init__(self, date_range):
        self.date_range = date_range
        self.date_one = date_range[0]
        self.date_two = date_range[1]

    def cash_flow(self):
        try:
            open(sqlite_file)
            conn = sqlite3.connect(sqlite_file)
            c =conn.cursor()
            sql = ('SELECT SUM(amount) FROM transactions WHERE date_time >= ? AND date_time <= ?')
            c.execute(sql,self.date_range)
            global csh_flow
            csh_flow = truncate(c.fetchone()[0],2)
            print (csh_flow)
            message_board = "-Cash_Flow calculated successfully- "
            return message_board
        except:
            message_board = "-Query was unsuccessful- "
            return message_board

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def app_setup(message):
    app = gui("Skitzer's Budget Tracker")
    app.setBg("grey")
    app.setFont(18)
    app.startLabelFrame("Budget Tracker")
    app.setSticky("w")
    app.addLabel("msgbrd", "Message board: ", 0, 0)
    app.addLabel("message board", message, 0, 1)
    app.getLabelWidget("msgbrd").config(font =8)
    app.getLabelWidget("message board").config(font=8)
    app.addLabel("title", "Welcome To Skitzer's Budget Tracker", 1, 0, 4)
    app.getLabelWidget("title").config(font= ("sans serif", "26"))
    app.setLabelAlign("title", "center")
    app.addLabel("total_amount", "Total amount in Bank: ", 2, 0)
    app.addLabel("total", total_amount , 2, 1)
    app.addLabel("net_flow", "Net flow gross for past month: ", 3,0)
    app.addLabel("nf", csh_flow, 3,1)

    app.startFrame("New Transactions")
    app.setSticky("ew")
    app.addLabel("new_transaction", "Enter a new transaction ",4,0)
    app.addLabelNumericEntry( "Amount: ", 5,0)
    def add_entry(btn):
        current_date = datetime.date.today()
        amount = truncate(app.getEntry("Amount: "),2)
        ctgry = app.getOptionBox("Category: ")
        cstm_message = app.getEntry("Custom Description: ")
        values = (current_date,amount,ctgry,cstm_message)
        update = Update_Database(values).update()
        app.clearEntry("Amount: ")
        app.clearEntry("Custom Description: ")
        message = update + ": " +amount + " - " + ctgry + " - "+ cstm_message
        app.setLabel("message board", message)
        current_date = datetime.date.today()
        one_month = current_date - (datetime.timedelta(days=30))
        dates = (one_month, current_date)
        CashFlow(dates).cash_flow()
        app.setLabel("total", total_amount)
        app.setLabel("nf", csh_flow)

    app.addLabelOptionBox("Category: ",["Rent" , "Utilities", "Groceries", "Fun", "Gas", "Subscriptions", "Bills",
                                        "Balance", "Deposit"], 7)
    app.addLabelEntry( "Custom Description: ", 8, 0)
    app.addButton("Add Entry", add_entry,9,0)

    app.go()




start = BtDatabase().create_db()
current_date = datetime.date.today()
one_month = current_date - (datetime.timedelta(days=30))
dates = (one_month,current_date)
cash_flow = CashFlow(dates).cash_flow()

message = start + cash_flow
print(message)
app_setup(message)

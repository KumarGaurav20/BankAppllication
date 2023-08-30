# Importing liabraries
import sqlite3
import uuid
import time
import datetime
import os

# Connecting the database
conn = sqlite3.connect('main.db')
cur= conn.cursor()

# Creating table "Records"
cur.execute('''
             
             CREATE TABLE IF NOT EXISTS RECORDS(
  NAME      VARCHAR(20)     NOT NULL, 
  Acc_No    CHAR(10)        NOT NULL, 
  Balance   INTEGER         NOT NULL, 
  PAN       CHAR(10)        NOT NULL, 
  Email     VARCHAR(20)     NOT NULL,
  PRIMARY KEY (Acc_No),
  UNIQUE (PAN, EMAIL)
);         
 ''')

# Creating table "Logs"          
cur.execute('''CREATE TABLE IF NOT EXISTS LOGS(
  Acc_No CHAR(10) NOT NULL, 
  T_id CHAR(10) NOT NULL, 
  Description CHAR(10) NOT NULL, 
  Sender VARCHAR(20) NOT NULL, 
  Reciever VARCHAR(20) NOT NULL, 
  DeAmt INTEGER, 
  CrAmount INTEGER, 
  Date_ DATE NOT NULL, 
  Time_ TIME NOT NULL, 
  PRIMARY KEY (T_id)
);
 ''') 
# datetime use 
conn.commit()

# Random no generator
def radnom_generator(n):
    return uuid.uuid1().hex[:n].upper()  
# to make sequential

# Creating Account
def createAccount():
    name= input('\t\t\t\t\tEnter your Name: \t')
    pan= input('\t\t\t\t\tEnter your PAN: \t')
    email_= input('\t\t\t\t\tEnter your Email: \t') 
    balance= int(input('\t\t\t\t\tEnter your balance: \t'))
    date_= datetime.datetime.now().strftime("%x")
    time_= datetime.datetime.now().strftime("%X")
    t_id= radnom_generator(10)
    acc_no1= radnom_generator(10)
    print(f"\t\t\t\t\tNAME: \t {name} \n PAN: \t {pan} \n BALANCE: {balance} \n DATE: \t {date_} \n TIME: \t {time_} \n Transanction ID: 123{t_id}")

    cur.execute(f''' 
                INSERT INTO "RECORDS" ("NAME", "Acc_No", "Balance", "PAN", "Email") VALUES ('{name}', '{acc_no1}', '{balance}', '{pan}', '{email_}');  
          ''') 
    cur.execute(f'''  
            INSERT INTO "LOGS" ("Acc_No", "T_id", "Description", "Sender", "Reciever", "CrAmount", "Date_", "Time_") VALUES ('{acc_no1}', '{t_id}', 'Self', '{name}', '{name}', '{balance}', '{date_}', '{time_}')  
          ''')
    conn.commit()   

def withdrawal():
    acc_no= input('\t\t\t\t\tEnter your Account number')
    name=input('\t\t\t\t\tEnter your name (Case Sensitive)')
    withdraw_amount=int(input("\t\t\t\t\tEnter the amount you want to withdraw"))
    self_balance= cur.execute(f''' 
                    SELECT Balance FROM RECORDS
                    WHERE NAME is '{name}';    
    ''')
    for x in self_balance:
        if x[0]< withdraw_amount:
            print('\t\t\t\t\tInsufficient Balance')
        else:
            t_id= radnom_generator(10)
            date_= datetime.datetime.now().strftime("%x")
# To make parameters streamlined
            time_= datetime.datetime.now().strftime("%X")
            cur.execute(f''' 
                INSERT INTO "LOGS" ("Acc_No", "T_id", "Description", "Sender", "Reciever", "DeAmt", "Date_", "Time_") VALUES ('{acc_no}', '{t_id}', 'self withdrawal', '{name}', '{name}', '{withdraw_amount}', '{date_}', '{time_}');
            ''')
            self_balance= cur.execute(f''' 
                    SELECT Balance FROM RECORDS
                    WHERE NAME is '{name}';    
            ''')
            balance2= balance_generator(self_balance)
            cur.execute(f''' 
                UPDATE RECORDS SET Balance= {balance2 - withdraw_amount} WHERE NAME is '{name}'
            ''')
            conn.commit()   

def deposit():
    acc_no= input('\t\t\t\t\tEnter your Account number')
    name=input('\t\t\t\t\tEnter your name (Case Sensitive)')
    deposit_amount=int(input("\t\t\t\t\tEnter the amount you want to deposit"))
    self_balance= cur.execute(f''' 
                    SELECT Balance FROM RECORDS
                    WHERE NAME is '{name}';    
    ''')
    for x in self_balance:
        if x[0]< deposit_amount:
            print('\t\t\t\t\tInsufficient Balance')
        else:
            t_id= radnom_generator(10)
            date_= datetime.datetime.now().strftime("%x")
# To make parameters streamlined
            time_= datetime.datetime.now().strftime("%X")
            cur.execute(f''' 
                INSERT INTO "LOGS" ("Acc_No", "T_id", "Description", "Sender", "Reciever", "CrAmount", "Date_", "Time_") VALUES ('{acc_no}', '{t_id}', 'self deposit', '{name}', '{name}', '{deposit_amount}', '{date_}', '{time_}');
            ''')
            self_balance= cur.execute(f''' 
                    SELECT Balance FROM RECORDS
                    WHERE NAME is '{name}';    
            ''')
            balance2= balance_generator(self_balance)
            cur.execute(f''' 
                UPDATE RECORDS SET Balance= {balance2 + deposit_amount} WHERE NAME is '{name}'
            ''')
            conn.commit()  

def transferMoney():
    acc_no1= input('\t\t\t\t\tEnter your Account number')
    name1=input('\t\t\t\t\tEnter your name (Case Sensitive)')
    acc_no2= input('\t\t\t\t\tEnter beneficiary Account number')
    name2= input('\t\t\t\t\tEnter beneficiary name')
    balance=int(input("\t\t\t\t\tEnter the amount you want to transfer"))
    a= cur.execute(f''' 
                    SELECT Balance FROM RECORDS
                    WHERE NAME is '{name1}';    
    ''')
    for x in a:
        if x[0]< balance:
            print('\t\t\t\t\tInsufficient Balance')
        else:
            t_id= radnom_generator(10)
            date_= datetime.datetime.now().strftime("%x")
# To make parameters streamlined
            time_= datetime.datetime.now().strftime("%X")
            cur.execute(f''' 
                INSERT INTO "LOGS" ("Acc_No", "T_id", "Description", "Sender", "Reciever", "DeAmt", "Date_", "Time_") VALUES ('{acc_no1}', '{t_id}', '{name1} sent {name2}', '{name1}', '{name2}', '{balance}', '{date_}', '{time_}');
            ''')
            recievers_balance= cur.execute(f''' 
                    SELECT Balance FROM RECORDS
                    WHERE NAME is '{name2}';    
            ''')
            balance2= balance_generator(recievers_balance)
            cur.execute(f''' 
                UPDATE RECORDS SET Balance= {balance2 + balance} WHERE NAME is '{name2}'
            ''')
            senders_balance= cur.execute(f''' 
                    SELECT Balance FROM RECORDS
                    WHERE NAME is '{name1}';    
            ''')  
            balance3= balance_generator(senders_balance)
            cur.execute(f''' 
                UPDATE RECORDS SET Balance= {balance3 - balance} WHERE NAME is '{name1}'
            ''')
            conn.commit() 
    
    # if( ''' There exist such account''' ):
    #     (''' Send the money into the account by: acc_no1 - amount, acc_no2+ amount, triggers enter logs (acc_no, descr, t_id, sender, reciever, debitor, creditor, date, time)''')
    # else:
    #     print("Wrong data entered")

def balance_generator(cursor_):
        for item_ in cursor_:
            _= item_[0]
            return _

def logs():
    account_name=input('\t\t\t\t\tEnter your name')
    log_holder=cur.execute(f'''
                    Select * FROM LOGS WHERE SENDER = '{account_name}' or RECIEVER= '{account_name}';
    ''')
    for i in log_holder:
        print("\033[1m" + f"\t\t\t\t\tAccount No: \t{i[0]}\n, \t\t\t\t\tT_id: \t{i[1]}\n,\t\t\t\t\tDescription: \t{i[2]}\n,\t\t\t\t\tSender: \t{i[3]}\n,\t\t\t\t\tReciever: \t{i[4]}\n,\t\t\t\t\tDebit Amount: \t{i[5]}\n,\t\t\t\t\tCredit Amount \t{i[6]}\n,\t\t\t\t\tDate: \t{i[7]}\n,\t\t\t\t\tTime: \t{i[8]}\n " + "\033[0m")

def statement():
    statement_name=input('\t\t\t\t\tEnter your name: ')
    statement_accNo=input('\t\t\t\t\tEnter your account no: ')
    statement_holder=cur.execute(f'''
                    Select * FROM RECORDS WHERE NAME = '{statement_name}' 
    ''')
    for x in statement_holder:
        fp= open("Statement.txt", "w+")
        fp.write("\033[1m" + "\n\t\t\t\t*****************************************************************************\n")
        fp.write("\t\t\t\t\t\t\t\tBANK STATEMENT\n")
        fp.write("\t\t\t\t*****************************************************************************\n")
        fp.write( "\t\t\t\t IFSC CODE: CBIN1029")
        fp.write("\t\t TOLL FREE NO: 11000")
        fp.write("\t BRANCH: KANJAHWALA\n\n"+ "\033[0m")
        fp.write('\t\t\t\t\tName:\t')
        fp.write(x[0])
        fp.write('\n\t\t\t\t\tAccount Number:\t')
        fp.write(x[1])
        fp.write('\n\t\t\t\t\tBalance:\t')
        fp.write(str(x[2]))
        fp.write('\n\t\t\t\t\tPAN:\t')
        fp.write(x[3])
        fp.write('\n\t\t\t\t\tEmail:\t\n')
        fp.write(x[4])
        fp.close()
    fp= open("Statement.txt", "r")
    print(fp.read())
    fp.close()


def intro_text():
    print("\n\t\t\t\t*********************************************************************************************************\t\t\t\t\t\t\t\t\t\t\t\t ")
    print(f'''\t\t\t\t 
\t\t\t\t ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
\t\t\t\t ██ ▄▄▀█ ▄▄▀█ ▄▄▀█ █▀████ ▄▀▄ █ ▄▄▀█ ▄▄▀█ ▄▄▀█ ▄▄▄█ ▄▄█ ▄▀▄ █ ▄▄█ ▄▄▀█▄ ▄████ ▄▄▄ █ ██ █ ▄▄█▄ ▄█ ▄▄█ ▄▀▄ 
\t\t\t\t ██ ▄▄▀█ ▀▀ █ ██ █ ▄▀████ █ █ █ ▀▀ █ ██ █ ▀▀ █ █▄▀█ ▄▄█ █▄█ █ ▄▄█ ██ ██ █████▄▄▄▀▀█ ▀▀ █▄▄▀██ ██ ▄▄█ █▄█ 
\t\t\t\t ██ ▀▀ █▄██▄█▄██▄█▄█▄████ ███ █▄██▄█▄██▄█▄██▄█▄▄▄▄█▄▄▄█▄███▄█▄▄▄█▄██▄██▄█████ ▀▀▀ █▀▀▀▄█▄▄▄██▄██▄▄▄█▄███▄
\t\t\t\t ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
''')
    print("\t\t\t\t*********************************************************************************************************\t\t\t\t\t\t\t\t\t\t\t\t \n")
def choices():
    print("\t\t\t\t\t------------------------\n")
    print("\033[1m" + "\t\t\t\t\tMAIN MENU" + "\033[0m")
    print("\t\t\t\t\t1. CREATE ACCOUNT")
    print("\t\t\t\t\t2. WITHDRAW AMOUNT")
    print("\t\t\t\t\t3. DEPOSIT AMOUNT")
    print("\t\t\t\t\t4. TRANSFER AMOUNT")
    print("\t\t\t\t\t5. ACCOUNT LOGS")
    print("\t\t\t\t\t6. STATEMENT")
    print("\t\t\t\t\t7. EXIT")
    print("\t\t\t\t\tSelect Your Option (1-8)\n")
    print("\t\t\t\t\t------------------------\n")

# Start of the program
ch='8'
num=0
intro_text()
try:
    while ch != 7:
        if num!=0:
            os.system("Clear")
            num+=1
        choices()    
        if ch == '1':
            createAccount()
        elif ch =='2':
            withdrawal()
        elif ch == '3':
            deposit()
        elif ch == '4':
            transferMoney()
        elif ch == '5':
            logs()
        elif ch == '6':
            statement()
        elif ch == '7':
            os.system('Clear')
            print("\t\t\t\t\t\t" + "\033[1m" +"Thanks for using bank managemnt system" +"\033[0m")
            break
        elif ch == '8':
            pass
        else :
            print("\t\t\t\t\tInvalid choice")
        ch = input("\t\t\t\t\tEnter your choice : ")
        os.system('Clear')
        print("\n")

except Exception as exc:
    print('\t\t\t\t\t', exc, '\n\t\t\t\t\t Try again')
import sqlite3

## Connect to database
conn = sqlite3.connect(':memory:')
c = conn.cursor()

## Create tables
c.execute("""CREATE TABLE budgets (creditcard integer, household integer, savings integer, rent integer, car integer, school integer)""")
c.execute("""CREATE TABLE creditcard (amount integer, payee text, category text, date date)""")
c.execute("""CREATE TABLE household (amount integer, payee text, category text, date date)""")
c.execute("""CREATE TABLE savings (amount integer, payee text, category text, date date)""")
c.execute("""CREATE TABLE rent (amount integer, payee text, category text, date date)""")
c.execute("""CREATE TABLE car (amount integer, payee text, category text, date date)""")
c.execute("""CREATE TABLE school (amount integer, payee text, category text, date date)""")

## Add a transaction
class Transaction:
    def __init__(self, amt, pay, cat, dat):
        self.amount = amt
        self.payee = pay
        self.category = cat
        self.date = dat

    def __repr__(self):
        return "({}, '{}', '{}', {})".format(self.amount, self.payee, self.category, self.date)

## FOR TESTING - Enter some data into tables
def insertData(transaction, account):
    with conn:
        c.execute("INSERT INTO " + account + " VALUES (:amt, :pay, :cat, :dat)",
                  {'amt': transaction.amount, 'pay': transaction.payee, 'cat': transaction.category, 'dat': transaction.date})

def checkEntry(account):
    total_net = []
    c.execute("SELECT * FROM " + account + " WHERE payee=:pay", {'pay': 'Dish'})
    check = c.fetchall()
    for entries in check:
        entry = entries[0]
        total_net.append(entry)
    print(sum(total_net))

new_entry = Transaction(100, 'Dish', 'Household', 20190814)
another_entry = Transaction(-80, 'Dish', 'Household', 20190814)
insertData(new_entry, 'household')
insertData(another_entry, 'household')
checkEntry('household')

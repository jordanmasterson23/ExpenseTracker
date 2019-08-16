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

def insertData(transaction, account):
    with conn:
        c.execute("INSERT INTO " + account + " VALUES (:amt, :pay, :cat, :dat)",
                  {'amt': transaction.amount, 'pay': transaction.payee,
                   'cat': transaction.category, 'dat': transaction.date})

def balance(account):
    total_net = []
    c.execute("SELECT * FROM " + account + " WHERE payee=:pay", {'pay': 'Dish'})
    check = c.fetchall()
    for entries in check:
        entry = entries[0]
        total_net.append(entry)
    return sum(total_net)

def newTransaction():
    choice = ''
    while choice not in 'e d'.split():
        choice = input("\nWhat kind of transaction do you want to make?\n"
                       "Enter 'E' to add an expense, 'I' to add income or 'T' to make a transfer: ").lower()
    if choice == 'e':
        expense()
    if choice == 'd':
        deposit()

def expense():
    amount = ''
    while type(amount) != int:
        try:
            amount = int(input('Amount: $'))
        except ValueError:
            print('Amount must be a number..')
    amount = -amount
    payee = input('Payee: ')
    category = input('Category: ')
    date = input('Date (YYYYMMDD): ')
    account = input('What account (creditcard, household, savings, rent, car, school): ').lower()
    transaction = Transaction(amount, payee, category, date)
    insertData(transaction, account)

def deposit():
    amount = ''
    while type(amount) != int:
        try:
            amount = int(input('Amount: $'))
        except ValueError:
            print('Amount must be a number..')
    payee = input('From: ')
    category = 'Deposit'
    date = input('Date (YYYYMMDD): ')
    account = input('What account (creditcard, household, savings, rent, car, school): ').lower()
    transaction = Transaction(amount, payee, category, date)
    insertData(transaction, account)

def overview():
    print("MY BUDGET & EXPENSES\n")
    print("ACCOUNT BALANCES")
    creditcard = str(balance('creditcard'))
    household = str(balance('household'))
    savings = str(balance('savings'))
    rent = str(balance('rent'))
    car = str(balance('car'))
    school = str(balance('school'))
    print("Credit Card: $" + creditcard)
    print("Household: $" + household)
    print("Savings: $" + savings)
    print("Rent: $" + rent)
    print("Car: $" + car)
    print("School: $" + school)

### TESTING
def TEST():
    new_entry = Transaction(100, 'Dish', 'Household', 20190814)
    another_entry = Transaction(-80, 'Dish', 'Household', 20190814)
    another_entry2 = Transaction(158, 'Dish', 'Household', 20190815)
    insertData(new_entry, 'household')
    insertData(another_entry, 'household')
    insertData(another_entry2, 'household')

# TEST()
overview()
newTransaction()
overview()
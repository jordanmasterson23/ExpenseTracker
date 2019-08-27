import sqlite3, sys

## Connect to database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

def main():
    try:
        c.execute("""CREATE TABLE budgets (spending integer, creditcard integer, household integer, savings integer, rent integer, car integer, school integer)""")
        c.execute("""CREATE TABLE spending (amount integer, payee text, category text, date date)""")
        c.execute("""CREATE TABLE creditcard (amount integer, payee text, category text, date date)""")
        c.execute("""CREATE TABLE household (amount integer, payee text, category text, date date)""")
        c.execute("""CREATE TABLE savings (amount integer, payee text, category text, date date)""")
        c.execute("""CREATE TABLE rent (amount integer, payee text, category text, date date)""")
        c.execute("""CREATE TABLE car (amount integer, payee text, category text, date date)""")
        c.execute("""CREATE TABLE school (amount integer, payee text, category text, date date)""")
        mainMenu()
    except sqlite3.OperationalError:
        mainMenu()

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
    c.execute("SELECT * FROM " + account)
    check = c.fetchall()
    for entries in check:
        entry = entries[0]
        total_net.append(entry)
    return sum(total_net)

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
    account = input('What account (spending, creditcard, household, savings, rent, car, school): ').lower()
    transaction = Transaction(amount, payee, category, date)
    insertData(transaction, account)
    mainMenu()

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
    account = input('What account (spending, creditcard, household, savings, rent, car, school): ').lower()
    transaction = Transaction(amount, payee, category, date)
    insertData(transaction, account)
    mainMenu()

def transfer():
    amount = ''
    while type(amount) != int:
        try:
            amount = int(input('Amount: $'))
        except ValueError:
            print('Amount must be a number..')
    amount1 = -amount
    account1 = input('What account do you want to transfer from: ').lower()
    account2 = input('What account do you want to transfer to: ').lower()
    payee1 = 'TRANSFER to ' + account2
    payee2 = 'TRANSFER from ' + account1
    category = 'Transfer'
    date = input('Date (YYYYMMDD): ')
    transaction1 = Transaction(amount1, payee1, category, date)
    insertData(transaction1, account1)
    transaction2 = Transaction(amount, payee2, category, date)
    insertData(transaction2, account2)
    mainMenu()

def viewAccount():
    account = input('What account do you want to view: ').lower()
    c.execute("SELECT * FROM " + account)
    check = c.fetchall()
    for entry in check:
        print('{}-{}-{}-{}'.format(str(entry[0]), entry[1], entry[2], str(entry[3])))
    mainMenu()

def mainMenu():
    print("MY BUDGET & EXPENSES\n")
    spending = str(balance('spending'))
    creditcard = str(balance('creditcard'))
    household = str(balance('household'))
    savings = str(balance('savings'))
    rent = str(balance('rent'))
    car = str(balance('car'))
    school = str(balance('school'))
    print("You have $" + spending + " to spend")
    print("Credit Card: $" + creditcard)
    print("Household: $" + household)
    print("Savings: $" + savings)
    print("Rent: $" + rent)
    print("Car: $" + car)
    print("School: $" + school)

    choice = ''
    while choice not in 'e i t v x'.split():
        choice = input("\nWhat would you like to do?\n"
                       "E - Add an Expense\n"
                       "I - Add Income\n"
                       "T - Make a transfer\n"
                       "V - View account info\n"
                       "X - Exit\n"
                       "\nEnter an option: ").lower()
    if choice == 'e':
        expense()
    if choice == 'i':
        deposit()
    if choice == 't':
        transfer()
    if choice == 'v':
        viewAccount()
    if choice == 'x':
        conn.close()
        quit()

def test():
    test1 = Transaction(1250, 'Dish Network', 'Paycheck', 20190816)
    test2 = Transaction(-150, 'Progressive', 'Insurance', 20190814)
    test3 = Transaction(-50, 'Shell', 'Gas', 20190810)
    test4 = Transaction(20, 'Rachel', 'Stuff', 20190815)
    test5 = Transaction(1233, 'Dish Network', 'Paycheck', 20190816)
    insertData(test1, 'Spending')
    insertData(test2, 'Spending')
    insertData(test3, 'Spending')
    insertData(test4, 'Spending')
    insertData(test5, 'Spending')

if __name__=="__main__":
    main()
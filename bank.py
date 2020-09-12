# Write your code here
import sqlite3
from random import randint

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"
INSERT_TABLE = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);"
FETCH_FROM_TABLE = "SELECT * FROM card WHERE number = ?;"
UPDATE_TABLE = "UPDATE card SET balance=? WHERE number=?;"
DELETE_FROM_TABLE = "DELETE FROM card WHERE number = ? AND pin = ?;"
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def create_table():
    cur.execute(CREATE_TABLE)
    conn.commit()


def insert_table(cn, pn, balance=0):
    cur.execute(INSERT_TABLE, (cn, pn, balance))
    conn.commit()


def fetch_row(cn):
    return cur.execute(FETCH_FROM_TABLE, (cn,)).fetchone()


def update_table(bal, cn):
    cur.execute(UPDATE_TABLE, (bal, cn))
    conn.commit()


def delete_table(cn, pn):
    cur.execute(DELETE_FROM_TABLE, (cn, pn))
    conn.commit()


def create_account():
    n = "\n"
    print("Your card has been created")
    temp_card_number = int("400000" + str(random_with_n_digits(9)))
    card_number = luhn_check(temp_card_number)
    pin_number = random_with_n_digits(4)
    print(f'Your card number:{n}{card_number}')
    print(f'Your card PIN:{n}{pin_number}')
    insert_table(card_number, pin_number)


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def luhn_check(cn):
    li = []
    for i in str(cn):
        li.append(int(i))
    for i in range(0, len(li), 2):
        li[i] *= 2
    for i in range(0, len(li)):
        if li[i] > 9:
            li[i] -= 9
    card_sum = sum(li)
    x_digit = 10 - (card_sum % 10)
    if x_digit == 10:
        x_digit = 0
    return int(str(cn) + str(x_digit))


def check_balance(cn):
    li = fetch_row(cn)
    balance = li[3]
    print(f'Balance: {balance}')


def add_income(cn):
    li = fetch_row(cn)
    balance = li[3]
    print("Enter income:")
    income = int(input())
    balance += income
    update_table(balance, cn)
    print("Income was added!")


def do_transfer(cn):
    print("Transfer")
    print("Enter card number:")
    r_card_number = int(input())
    number = str(r_card_number)
    check_number = int(number[0:15])
    c_li = fetch_row(cn)
    r_li = fetch_row(r_card_number)
    if r_card_number == cn:
        print("You can't transfer money to the same account!")
    elif luhn_check(check_number) != r_card_number:
        print("Probably you made a mistake in the card number. Please try again!")
    elif not r_li:
        print("Such a card does not exist.")
    else:
        print("Enter how much money you want to transfer:")
        amount = int(input())
        if amount > c_li[3]:
            print("Not enough money!")
        else:
            r_balance = r_li[3] + amount
            c_balance = c_li[3] - amount
            update_table(r_balance, r_card_number)
            update_table(c_balance, cn)
            print("Success!")


def close_account(cn, pn):
    delete_table(cn, pn)
    print("The account has been closed!")


def log_out():
    print("You have successfully logged out!")


def account_details(cn, pn):
    card_number = cn
    pin_number = pn
    print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
    while True:
        ac_choice = int(input())
        if ac_choice == 1:
            check_balance(card_number)
        elif ac_choice == 2:
            add_income(card_number)
        elif ac_choice == 3:
            do_transfer(card_number)
        elif ac_choice == 4:
            close_account(card_number, pin_number)
            break
        elif ac_choice == 5:
            log_out()
            break
        elif ac_choice == 0:
            exit_account()


def log_account():
    print("Enter your card number:")
    card_number = int(input())
    print("Enter your PIN:")
    pin_number = int(input())
    li = fetch_row(card_number)
    if li and int(li[2]) == pin_number:
        print('You have successfully logged in!')
        account_details(card_number, pin_number)
    else:
        print("Wrong card number or PIN!")


def exit_account():
    print("Bye!")
    exit()


def menu():
    create_table()
    print("1. Create an account\n2. Log into account\n0. Exit")
    while True:
        user_choice = int(input())
        if user_choice == 1:
            create_account()
        elif user_choice == 2:
            log_account()
        elif user_choice == 0:
            exit_account()


if __name__ == "__main__":
    menu()

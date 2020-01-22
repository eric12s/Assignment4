import sqlite3
import os
import atexit
import sys


def create_tables():
    cursor.execute("""
         CREATE TABLE Employees(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL,
            coffee_stand INTEGER REFERENCES Coffee_stands(id)
        )""")

    cursor.execute("""
        CREATE TABLE Suppliers(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_information TEXT
)""")

    cursor.execute("""
        CREATE TABLE Products(
            id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )""")

    cursor.execute("""
        CREATE TABLE Coffee_stands(
            id INTEGER PRIMARY KEY,
            location TEXT NOT NULL,
            number_of_employees INTEGER
        )""")

    cursor.execute("""
        CREATE TABLE Activities(
            product_id INTEGER INTEGER REFERENCES Products(id),
            quantity INTEGER NOT NULL,
            activator_id INTEGER NOT NULL,
            date DATE NOT NULL 
        )""")


def insert_employees(id, name, salary, coffee_stand):
    cursor.execute("INSERT INTO Employees VALUES (?,?,?,?)", [id, name, salary, coffee_stand])


def insert_suppliers(id, name, contact_information):
    cursor.execute("INSERT INTO Suppliers VALUES (?,?,?)", [id, name, contact_information])


def insert_products(id, description, price, quantity=0):
    cursor.execute("INSERT INTO Products VALUES (?,?,?,?)", [id, description, price, quantity])


def insert_coffee_stands(id, location, number_of_employees):
    cursor.execute("INSERT INTO Coffee_stands VALUES (?,?,?)", [id, location, number_of_employees])


def insert_activities(product_id, quantity, activator_id, date):
    cursor.execute("INSERT INTO Activities VALUES (?,?,?,?)", [product_id, quantity, activator_id, date])

def insert_data():
    with open(sys.argv[1]) as inputfile:
        for line in inputfile:
            line = line.strip()
            line = line.split(", ")
            table = line[0]
            data = line[1:]
            if table == "C":
                insert_coffee_stands(*data)
            if table == "S":
                insert_suppliers(*data)
            if table == "E":
                insert_employees(*data)
            if table == "P":
                insert_products(*data)


if __name__ == '__main__':
    DBExist = os.path.isfile('moncafe.db')
    if DBExist:
        os.remove('moncafe.db')

    dbcon = sqlite3.connect('moncafe.db')
    cursor = dbcon.cursor()
    create_tables()
    insert_data()


def close_db():
    dbcon.commit()
    dbcon.close()


atexit.register(close_db)
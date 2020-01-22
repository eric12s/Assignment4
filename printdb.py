import os
import sqlite3

if __name__ == "__main__":
    if os.path.isfile("moncafe.db"):
        dbcon = sqlite3.connect("moncafe.db")
        cursor = dbcon.cursor()

        tables = ["Activities", "Coffee_stands", "Employees", "Products", "Suppliers"]
        for table in tables:
            print(table)
            cursor.execute("SELECT * FROM " + table)
            list = cursor.fetchall()
            for row in list:
                print(row)

        print('\nEmployees report')
        table = cursor.execute(
            """SELECT name, salary, location, ifnull(counter,0) FROM Employees
            LEFT JOIN Coffee_stands ON Coffee_stands.id = coffee_stand
            LEFT JOIN (SELECT activator_id, COUNT(*) as counter FROM Activities GROUP BY activator_id)
            ORDER BY name
            """).fetchall()
        for row in table:
            print("{} {} {} {}".format(row[0], row[1], row[2], row[3]))

        print('\nActivities')
        table = cursor.execute(
            """SELECT Activities.date,Products.description,Activities.quantity,Employees.name,Suppliers.name 
            FROM Activities
                   LEFT JOIN Products ON Products.id = product_id
                   LEFT JOIN Employees ON Employees.id = activator_id
                   LEFT JOIN Suppliers ON Suppliers.id = activator_id
                   ORDER BY date
        """)
        table.fetchall()
        for row in table:
            print(row)

        cursor.close()



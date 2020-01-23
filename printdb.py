import os
import sqlite3


def main():
    if os.path.isfile("moncafe.db"):
        dbcon = sqlite3.connect("moncafe.db")
        cursor = dbcon.cursor()

        tables = ["Activities", "Coffee_stands", "Employees", "Products", "Suppliers"]
        for table in tables:
            if table == "Activities":
                print(table)
                cursor.execute("""SELECT * FROM Activities ORDER BY date""")
                list = cursor.fetchall()
                for row in list:
                    print(row)

            elif table == "Coffee_stands":
                print("Coffee stands")
                cursor.execute("SELECT * FROM " + table)
                list = cursor.fetchall()
                for row in list:
                    print(row)

            else:
                print(table)
                cursor.execute("SELECT * FROM " + table)
                list = cursor.fetchall()
                for row in list:
                    print(row)

        print('\nEmployees report')
        table = cursor.execute(
            """SELECT name, salary, location, ifnull(counter,0) FROM Employees
            LEFT JOIN Coffee_stands ON Coffee_stands.id = coffee_stand
            LEFT JOIN (SELECT activator_id, SUM((SELECT price FROM Products WHERE product_id = id) * quantity) * (-1) as counter FROM Activities GROUP BY activator_id)
            ON activator_id=Employees.id ORDER BY name
            """).fetchall()
        for row in table:
            print("{} {} {} {}".format(row[0], row[1], row[2], row[3]))

        cursor.execute("""SELECT COUNT(*) from Activities LIMIT 1""")
        isExist = cursor.fetchall()
        if isExist[0][0] > 0:
            print('\nActivities')
            table = cursor.execute(
                """SELECT Activities.date, Products.description, Activities.quantity, Employees.name, Suppliers.name 
                FROM Activities
                LEFT JOIN Products ON Products.id = product_id
                LEFT JOIN Employees ON Employees.id = activator_id
                LEFT JOIN Suppliers ON Suppliers.id = activator_id
                ORDER BY date
            """).fetchall()
            for row in table:
                print(row)

        dbcon.close()


if __name__ == "__main__":
    main()



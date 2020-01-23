import os
import sqlite3
import sys
import printdb


if __name__ == "__main__":
    if os.path.isfile("moncafe.db"):
        dbcon = sqlite3.connect("moncafe.db")
        cursor = dbcon.cursor()
        with open(sys.argv[1]) as inputfile:
            for line in inputfile:
                line = line.strip()
                line = line.replace(', ', ',')
                line = line.split(",")
                if int(line[1]) > 0:
                    product_id = line[0]
                    quantityAdded = line[1]
                    supplierID = line[2]
                    date = line[3]
                    cursor.execute("""
                    UPDATE Products SET quantity=(quantity+?) WHERE id=(?)""", [quantityAdded, product_id])
                    cursor.execute("""
                    INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)""",
                                   [product_id, quantityAdded, supplierID, date])

                elif int(line[1]) < 0:
                    product_id = line[0]
                    quantityReduced = line[1]
                    employeeID = line[2]
                    date = line[3]
                    initQuantity = cursor.execute("""SELECT quantity FROM Products WHERE id=(?)""",
                                                  [product_id]).fetchone()
                    if (int(initQuantity[0]) + int(quantityReduced)) >= 0:
                        cursor.execute("""
                        UPDATE Products SET quantity=(quantity+?) WHERE id=(?)""", [quantityReduced, product_id])
                        cursor.execute("""
                        INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)""",
                                       [product_id, quantityReduced, employeeID, date])

        dbcon.commit()
        dbcon.close()
        printdb.main()
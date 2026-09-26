# Assignment 4: Menu-driven program - CRUD operations on Employee table
# in a database, using pandas + SQLite

import sqlite3
import pandas as pd

DB_NAME = "employee.db"
TABLE = "employee"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table_if_missing():
    conn = get_connection()
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            department TEXT,
            salary REAL
        )
    """)
    conn.commit()
    conn.close()

def add_employee():
    emp_id = int(input("Enter Employee ID: "))
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    dept = input("Enter Department: ")
    salary = float(input("Enter Salary: "))

    df = pd.DataFrame([[emp_id, name, age, dept, salary]],
                    columns=["emp_id", "name", "age", "department", "salary"])

    conn = get_connection()
    df.to_sql(TABLE, conn, if_exists="append", index=False)
    conn.close()
    print("Employee added successfully!\n")

def view_employees():
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {TABLE}", conn)
    conn.close()

    if df.empty:
        print("No employee records found.\n")
    else:
        print(df.to_string(index=False))
        print()

def update_employee():
    emp_id = int(input("Enter Employee ID to update: "))
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {TABLE} WHERE emp_id={emp_id}", conn)

    if df.empty:
        print("Employee ID not found.\n")
        conn.close()
        return

    name = input("Enter new Name: ")
    age = int(input("Enter new Age: "))
    dept = input("Enter new Department: ")
    salary = float(input("Enter new Salary: "))

    conn.execute(
        f"""UPDATE {TABLE} SET name=?, age=?, department=?, salary=?
            WHERE emp_id=?""",
        (name, age, dept, salary, emp_id)
    )
    conn.commit()
    conn.close()
    print("Employee updated successfully!\n")

def delete_employee():
    emp_id = int(input("Enter Employee ID to delete: "))
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {TABLE} WHERE emp_id={emp_id}", conn)

    if df.empty:
        print("Employee ID not found.\n")
        conn.close()
        return

    conn.execute(f"DELETE FROM {TABLE} WHERE emp_id=?", (emp_id,))
    conn.commit()
    conn.close()
    print("Employee deleted successfully!\n")

def menu():
    create_table_if_missing()
    while True:
        print("---- Employee Database CRUD Menu (pandas) ----")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            update_employee()
        elif choice == "4":
            delete_employee()
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.\n")
            
if __name__ == "__main__":
    menu()

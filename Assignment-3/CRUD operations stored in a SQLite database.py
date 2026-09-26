# Assignment 3: Menu-driven program - class to perform CRUD operations
# on an Employee table stored in a SQLite database.

# Employee table fields: emp_id, name, age, dept, salary

import sqlite3
DB_FILE = "employee.db"

class EmployeeDB:
    def __init__(self, db_file=DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                emp_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                dept TEXT,
                salary REAL
            )
        """)
        self.conn.commit()
# create
    def add_employee(self, emp_id, name, age, dept, salary):
        try:
            self.cursor.execute(
                "INSERT INTO employee VALUES (?, ?, ?, ?, ?)",
                (emp_id, name, age, dept, salary)
            )
            self.conn.commit()
            print("Employee record added successfully.")
        except sqlite3.IntegrityError:
            print(f"Employee with ID {emp_id} already exists. Choose a different ID.")
# read
    def view_all(self):
        self.cursor.execute("SELECT * FROM employee")
        rows = self.cursor.fetchall()
        if not rows:
            print("No records found.")
            return
        print(f"\n{'ID':<8}{'Name':<15}{'Age':<6}{'Dept':<15}{'Salary':<10}")
        print("-" * 54)
        for r in rows:
            print(f"{r[0]:<8}{r[1]:<15}{r[2]:<6}{r[3]:<15}{r[4]:<10}")

    def view_one(self, emp_id):
        self.cursor.execute("SELECT * FROM employee WHERE emp_id = ?", (emp_id,))
        row = self.cursor.fetchone()
        if row:
            print(row)
        else:
            print(f"Employee with ID {emp_id} not found.")
        return row

# update
    def update_employee(self, emp_id, name=None, age=None, dept=None, salary=None):
        fields, values = [], []
        if name:
            fields.append("name = ?")
            values.append(name)
        if age:
            fields.append("age = ?")
            values.append(age)
        if dept:
            fields.append("dept = ?")
            values.append(dept)
        if salary:
            fields.append("salary = ?")
            values.append(salary)

        if not fields:
            print("Nothing to update.")
            return

        values.append(emp_id)
        query = f"UPDATE employee SET {', '.join(fields)} WHERE emp_id = ?"
        self.cursor.execute(query, tuple(values))
        self.conn.commit()

        if self.cursor.rowcount:
            print("Employee record updated successfully.")
        else:
            print(f"Employee with ID {emp_id} not found.")

# delete
    def delete_employee(self, emp_id):
        self.cursor.execute("DELETE FROM employee WHERE emp_id = ?", (emp_id,))
        self.conn.commit()
        if self.cursor.rowcount:
            print("Employee record deleted successfully.")
        else:
            print(f"Employee with ID {emp_id} not found.")

    def close(self):
        self.conn.close()


def get_int(prompt):
    """Helper: keep asking until the user enters a valid integer, or '' to skip."""
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid whole number.")


def get_float(prompt):
    """Helper: keep asking until the user enters a valid number, or '' to skip."""
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def menu():
    db = EmployeeDB()
    try:
        while True:
            print("\n----- Employee Database CRUD Menu -----")
            print("1. Add Employee (Create)")
            print("2. View All Employees (Read)")
            print("3. View One Employee (Read)")
            print("4. Update Employee (Update)")
            print("5. Delete Employee (Delete)")
            print("6. Exit")
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                emp_id = get_int("Enter Employee ID: ")
                name = input("Enter Name: ").strip()
                age = get_int("Enter Age: ")
                dept = input("Enter Department: ").strip()
                salary = get_float("Enter Salary: ")
                db.add_employee(emp_id, name, age, dept, salary)

            elif choice == "2":
                db.view_all()

            elif choice == "3":
                emp_id = get_int("Enter Employee ID to search: ")
                db.view_one(emp_id)

            elif choice == "4":
                emp_id = get_int("Enter Employee ID to update: ")
                name = input("New Name (leave blank to skip): ").strip()
                age = get_int("New Age (leave blank to skip): ")
                dept = input("New Department (leave blank to skip): ").strip()
                salary = get_float("New Salary (leave blank to skip): ")
                db.update_employee(emp_id, name or None, age, dept or None, salary)

            elif choice == "5":
                emp_id = get_int("Enter Employee ID to delete: ")
                db.delete_employee(emp_id)

            elif choice == "6":
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please try again.")
    finally:
        db.close()

if __name__ == "__main__":
    menu()

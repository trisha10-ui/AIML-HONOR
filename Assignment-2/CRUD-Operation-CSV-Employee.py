# Assignment 2: Menu-driven program - class to perform CRUD operations
# on an Employee table stored in a CSV file (using Python's built-in
# csv/file handling module).

# Employee record fields: emp_id, name, department, salary

import csv
import os

FILENAME = "employee.csv"
FIELDS = ["emp_id", "name", "department", "salary"]


class EmployeeCSV:
    def __init__(self, filename=FILENAME):
        self.filename = filename
        # Create file with header if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()

    def _read_all(self):
        with open(self.filename, "r", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _write_all(self, rows):
        with open(self.filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

#create employee file
    def create(self, emp_id, name, department, salary):
        rows = self._read_all()
        if any(r["emp_id"] == str(emp_id) for r in rows):
            print(f"Employee with ID {emp_id} already exists.")
            return
        with open(self.filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writerow({
                "emp_id": emp_id, "name": name,
                "department": department, "salary": salary
            })
        print("Employee record added successfully.")
#read file
    def read_all(self):
        rows = self._read_all()
        if not rows:
            print("No records found.")
            return
        print(f"\n{'ID':<8}{'Name':<20}{'Department':<15}{'Salary':<10}")
        print("-" * 53)
        for r in rows:
            print(f"{r['emp_id']:<8}{r['name']:<20}{r['department']:<15}{r['salary']:<10}")

    def read_one(self, emp_id):
        rows = self._read_all()
        for r in rows:
            if r["emp_id"] == str(emp_id):
                print(r)
                return r
        print(f"Employee with ID {emp_id} not found.")
        return None
#update employe detailes

    def update(self, emp_id, name=None, department=None, salary=None):
        rows = self._read_all()
        found = False
        for r in rows:
            if r["emp_id"] == str(emp_id):
                found = True
                if name:
                    r["name"] = name
                if department:
                    r["department"] = department
                if salary:
                    r["salary"] = salary
        if found:
            self._write_all(rows)
            print("Employee record updated successfully.")
        else:
            print(f"Employee with ID {emp_id} not found.")

#delete details
    def delete(self, emp_id):
        rows = self._read_all()
        new_rows = [r for r in rows if r["emp_id"] != str(emp_id)]
        if len(new_rows) == len(rows):
            print(f"Employee with ID {emp_id} not found.")
        else:
            self._write_all(new_rows)
            print("Employee record deleted successfully.")
#menu

def menu():
    emp = EmployeeCSV()
    while True:
        print("\n----- Employee CSV CRUD Menu -----")
        print("1. Add Employee (Create)")
        print("2. View All Employees (Read)")
        print("3. View One Employee (Read)")
        print("4. Update Employee (Update)")
        print("5. Delete Employee (Delete)")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            emp_id = input("Enter Employee ID: ").strip()
            name = input("Enter Name: ").strip()
            department = input("Enter Department: ").strip()
            salary = input("Enter Salary: ").strip()
            emp.create(emp_id, name, department, salary)

        elif choice == "2":
            emp.read_all()

        elif choice == "3":
            emp_id = input("Enter Employee ID to search: ").strip()
            emp.read_one(emp_id)

        elif choice == "4":
            emp_id = input("Enter Employee ID to update: ").strip()
            name = input("New Name (leave blank to skip): ").strip()
            department = input("New Department (leave blank to skip): ").strip()
            salary = input("New Salary (leave blank to skip): ").strip()
            emp.update(emp_id, name or None, department or None, salary or None)

        elif choice == "5":
            emp_id = input("Enter Employee ID to delete: ").strip()
            emp.delete(emp_id)

        elif choice == "6":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()

import csv
import os
import pandas as pd

FILE_NAME = "employees.csv"

class EmployeeManager:
    def __init__(self):
        # create file with headers if it doesn't exist
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Department", "Salary"])

    def add_employee(self):
        emp_id = input("Enter Employee ID: ")
        
        if self.find_employee(emp_id):
            print("Error: Employee ID already exists!")
            return

        name = input("Enter Name: ")
        dept = input("Enter Department: ")
        salary = input("Enter Salary: ")

        with open(FILE_NAME, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([emp_id, name, dept, salary])
        
        print("Employee added.")

    def view_employees(self):
        try:
            data = pd.read_csv(FILE_NAME)
            if data.empty:
                print("No records found.")
            else:
                print("\n--- Employee List ---")
                print(data.to_string(index=False))
                print("---------------------\n")
        except Exception as e:
            print("Error reading file:", e)

    def find_employee(self, emp_id):
        with open(FILE_NAME, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == emp_id:
                    return row
        return None

    def update_employee(self):
        emp_id = input("Enter Employee ID to update: ")
        rows = []
        found = False
        
        with open(FILE_NAME, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == emp_id:
                    found = True
                    print(f"Old Data -> Name: {row[1]}, Dept: {row[2]}, Salary: {row[3]}")
                    
                    name = input("Enter new Name (or press enter to skip): ")
                    dept = input("Enter new Department (or press enter to skip): ")
                    salary = input("Enter new Salary (or press enter to skip): ")

                    if name == "": name = row[1]
                    if dept == "": dept = row[2]
                    if salary == "": salary = row[3]
                    
                    rows.append([emp_id, name, dept, salary])
                else:
                    rows.append(row)

        if not found:
            print("Employee not found.")
            return

        with open(FILE_NAME, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print("Employee updated.")

    def delete_employee(self):
        emp_id = input("Enter Employee ID to delete: ")
        rows = []
        found = False
        
        with open(FILE_NAME, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == emp_id:
                    found = True
                else:
                    rows.append(row)

        if not found:
            print("Employee not found.")
            return

        with open(FILE_NAME, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print("Employee deleted.")

# Menu Loop
if __name__ == "__main__":
    manager = EmployeeManager()
    
    while True:
        print("1. Add Employee")
        print("2. View Employees (Pandas)")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            manager.add_employee()
        elif choice == '2':
            manager.view_employees()
        elif choice == '3':
            manager.update_employee()
        elif choice == '4':
            manager.delete_employee()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

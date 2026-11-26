import csv
import os

# name of the file we are using
FILE_NAME = "employees.csv"

class EmployeeManager:
    def __init__(self):
        # create the file with headers if it doesn't exist
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Department", "Salary"])

    def add_employee(self):
        emp_id = input("Enter Employee ID: ")
        
        # check if id already exists
        if self.find_employee(emp_id):
            print("Error: Employee ID already exists!")
            return

        name = input("Enter Name: ")
        dept = input("Enter Department: ")
        salary = input("Enter Salary: ")

        with open(FILE_NAME, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([emp_id, name, dept, salary])
        
        print("Employee added successfully.")

    def view_employees(self):
        with open(FILE_NAME, mode='r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            if len(rows) <= 1:
                print("No employees found.")
                return

            print("\n--- Employee List ---")
            for row in rows:
                # print nicely formatted
                print(f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Salary: {row[3]}")
            print("---------------------\n")

    def find_employee(self, emp_id):
        # helper function to return the employee row if found
        with open(FILE_NAME, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == emp_id:
                    return row
        return None

    def update_employee(self):
        emp_id = input("Enter Employee ID to update: ")
        
        # read all data first
        rows = []
        found = False
        
        with open(FILE_NAME, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == emp_id:
                    found = True
                    print(f"Current Data -> Name: {row[1]}, Dept: {row[2]}, Salary: {row[3]}")
                    
                    # ask for new data
                    name = input("Enter new Name (or press enter to keep old): ")
                    dept = input("Enter new Department (or press enter to keep old): ")
                    salary = input("Enter new Salary (or press enter to keep old): ")

                    if name == "": name = row[1]
                    if dept == "": dept = row[2]
                    if salary == "": salary = row[3]
                    
                    rows.append([emp_id, name, dept, salary])
                else:
                    rows.append(row)

        if not found:
            print("Employee not found.")
            return

        # write everything back
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
                    # skip this row (don't add to new list)
                else:
                    rows.append(row)

        if not found:
            print("Employee not found.")
            return

        # write remaining rows back
        with open(FILE_NAME, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
            
        print("Employee deleted.")

# Nenu Loop
if __name__ == "__main__":
    manager = EmployeeManager()
    
    while True:
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            manager.add_employee()
        elif choice == '2':
            manager.view_employees()
        elif choice == '3':
            manager.update_employee()
        elif choice == '4':
            manager.delete_employee()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

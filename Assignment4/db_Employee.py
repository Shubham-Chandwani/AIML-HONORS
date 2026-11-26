import sqlite3
import pandas as pd

class Employee:
    def __init__(self, emp_id, name, dept, salary):
        self.emp_id = emp_id
        self.name = name
        self.dept = dept
        self.salary = salary

    def __str__(self):
        return f"ID: {self.emp_id} | Name: {self.name} | Dept: {self.dept} | Salary: {self.salary}"


class EmployeeDAO:
    def __init__(self):
        self.conn = sqlite3.connect("company_assign4.db")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department TEXT,
                salary REAL
            )
        """)
        self.conn.commit()

    def add(self, emp):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO employee (id, name, department, salary) VALUES (?, ?, ?, ?)",
                (emp.emp_id, emp.name, emp.dept, emp.salary)
            )
            self.conn.commit()
            print("Employee added successfully.")
        except sqlite3.IntegrityError:
            print("Error: Employee ID already exists.")
        except Exception as e:
            print("Error adding employee:", e)

    def get_all_pandas(self):
        # USING PANDAS HERE to read the whole table
        query = "SELECT * FROM employee"
        df = pd.read_sql_query(query, self.conn)
        
        if df.empty:
            print("No records found.")
        else:
            print("\n--- Employee List ---")
            print(df.to_string(index=False)) # prints it like a clean table
            print("---------------------")

    def get_by_id(self, emp_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE id = ?", (emp_id,))
        row = cursor.fetchone()
        
        if row:
            return Employee(row[0], row[1], row[2], row[3])
        return None

    def update(self, emp):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE employee SET name = ?, department = ?, salary = ? WHERE id = ?",
            (emp.name, emp.dept, emp.salary, emp.emp_id)
        )
        self.conn.commit()
        print("Employee updated successfully.")

    def delete(self, emp_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM employee WHERE id = ?", (emp_id,))
        self.conn.commit()
        print("Employee deleted successfully.")

    def close(self):
        self.conn.close()


# --- Menu Logic ---
if __name__ == "__main__":
    dao = EmployeeDAO()
    
    while True:
        print("\n--- Employee Management System ---")
        print("1. Add Employee")
        print("2. View All Employees (Pandas Table)")
        print("3. Search Employee by ID")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            eid = int(input("Enter ID: "))
            name = input("Enter Name: ")
            dept = input("Enter Dept: ")
            sal = float(input("Enter Salary: "))
            
            new_emp = Employee(eid, name, dept, sal)
            dao.add(new_emp)
            
        elif choice == '2':
            # Call the pandas function here
            dao.get_all_pandas()
                    
        elif choice == '3':
            eid = int(input("Enter ID to search: "))
            emp = dao.get_by_id(eid)
            if emp:
                print("Found:", emp)
            else:
                print("Employee not found.")
                
        elif choice == '4':
            eid = int(input("Enter ID to update: "))
            emp = dao.get_by_id(eid)
            if emp:
                print("Current:", emp)
                emp.name = input("Enter new Name: ")
                emp.dept = input("Enter new Dept: ")
                emp.salary = float(input("Enter new Salary: "))
                dao.update(emp)
            else:
                print("Employee not found.")
                
        elif choice == '5':
            eid = int(input("Enter ID to delete: "))
            dao.delete(eid)
            
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")
            
    dao.close()

import sqlite3

class EmployeeDB:
    def __init__(self):
        # connects to the file. If it doesn't exist, it creates it.
        self.conn = sqlite3.connect("company.db")
        self.create_table()

    def create_table(self):
        # make sure the table exists before we do anything
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

    def add_employee(self):
        emp_id = input("Enter Employee ID: ")
        name = input("Enter Name: ")
        dept = input("Enter Department: ")
        
        try:
            salary = float(input("Enter Salary: "))
        except ValueError:
            print("Invalid salary amount.")
            return

        try:
            cursor = self.conn.cursor()
            # using ? for sqlite instead of %s
            cursor.execute(
                "INSERT INTO employee (id, name, department, salary) VALUES (?, ?, ?, ?)", 
                (emp_id, name, dept, salary)
            )
            self.conn.commit()
            print("Employee added.")
        except sqlite3.IntegrityError:
            # this happens if you try to add an ID that already exists
            print("Error: Employee ID already exists.")
        except Exception as e:
            print("Error:", e)

    def view_employees(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employee")
        rows = cursor.fetchall()
        
        if len(rows) == 0:
            print("No employees found.")
            return
            
        print("\n--- Employee List ---")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Salary: {row[3]}")
        print("---------------------\n")

    def update_employee(self):
        emp_id = input("Enter Employee ID to update: ")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE id = ?", (emp_id,))
        result = cursor.fetchone()
        
        if not result:
            print("Employee not found.")
            return
            
        print("Current Details -> Name:", result[1], "| Dept:", result[2], "| Salary:", result[3])
        
        name = input("Enter new Name: ")
        dept = input("Enter new Department: ")
        
        try:
            salary = float(input("Enter new Salary: "))
        except ValueError:
            print("Invalid salary amount.")
            return

        cursor.execute(
            "UPDATE employee SET name = ?, department = ?, salary = ? WHERE id = ?",
            (name, dept, salary, emp_id)
        )
        self.conn.commit()
        print("Employee updated.")

    def delete_employee(self):
        emp_id = input("Enter Employee ID to delete: ")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE id = ?", (emp_id,))
        if not cursor.fetchone():
            print("Employee not found.")
            return

        cursor.execute("DELETE FROM employee WHERE id = ?", (emp_id,))
        self.conn.commit()
        print("Employee deleted.")

# --- Menu ---
if __name__ == "__main__":
    db = EmployeeDB()
    
    while True:
        print("\n1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            db.add_employee()
        elif choice == '2':
            db.view_employees()
        elif choice == '3':
            db.update_employee()
        elif choice == '4':
            db.delete_employee()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")
    
    # close connection when done
    db.conn.close()

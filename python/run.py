import os
import pickle


class Employee:
    def __init__(self, name, id, title, department) -> None:
        self.name = name
        self.id = id
        self.title = title
        self.department = department

    def display_employee(self):
        print("ID      Name         Title         Department")
        print(self.id, self.name, self.title, self.department)

    def __str__(self) -> str:
        return f"Name: {self.name}, ID: {self.id}"


class Department:
    def __init__(self, name) -> None:
        self.name = name
        self.employees = {}

    def add_an_employee(self):
        name = input("Enter Employee name: ")
        id = input("Enter Employee ID: ")
        title = input("Enter Employee Title: ")
        employee = Employee(name, id, title, self.name)
        self.employees[employee.id] = employee

    def remove_an_employee(self):
        id = input("Enter Employee ID: ")
        self.employees.pop(id)
        print(f"Employee {id} removed!")

    def list_all_employees(self):
        return list(self.employees.values())

class CompanyClass:
    company = {}

    @classmethod
    def add_a_department(cls):
        print("Enter following details-")
        department_name = input("Enter Department Name to add: ")
        cls.company[department_name] = Department(department_name)
        print("added a department!")

    @classmethod
    def add_an_employee(cls):
        department_name = input("Enter Department Name of Employee: ")
        if department_name not in cls.company:
            raise Exception(f"{department_name} does not exist in Departments")
        cls.company[department_name].add_an_employee()
        print("added an employee!")

    @classmethod
    def remove_an_employee(cls):
        department_name = input("Enter Department Name of Employee: ")
        if department_name not in cls.company:
            raise Exception(f"{department_name} does not exist in Departments")
        cls.company[department_name].remove_an_employee()
        print("removed an employee!")

    @classmethod
    def display_all_departments(cls):
        print("Following are the departments names-")
        for department in cls.company:
            print(department)

    @classmethod
    def display_a_department_details(cls):
        name = input("Enter Department Name: ")
        print("Employees:")
        if name not in cls.company:
            raise Exception(f"{name} does not exist in Departments")
        for employee in cls.company[name].list_all_employees():
            employee.display_employee()

    @classmethod
    def save_records(cls):
        with open("saved_records.obj", "wb") as records:
            pickle.dump(cls.company, records)

    @classmethod
    def load_records(cls):
        if os.path.exists("saved_records.obj"):
            with open("saved_records.obj", "rb") as records:
                cls.company = pickle.load(records)


if __name__ == "__main__":
    company = CompanyClass()
    company.load_records()
    while True:
        print("--------------------------")
        print("Employee Management System")
        print("--------------------------")
        print("Choose one of the following options")
        options = ["1. add_a_department", "2. remove_a_department", "3. display_all_departments",
                "4. display_a_department_details", "5. Add an Employee", "6. Remove an Employee"]
        for option in options:
            print(option)
        
        while True:
            selected_index = int(input("Enter the index number: "))
            if selected_index < 1 or selected_index > 6:
                print(f"Option can not be {selected_index}, please select from", [i for i in range(1, 7)])
                continue
            break
        try:
            if selected_index == 1:
                company.add_a_department()
            if selected_index == 2:
                company.remove_a_department()
            if selected_index == 3:
                company.display_all_departments()
            if selected_index == 4:
                company.display_a_department_details()
            if selected_index == 5:
                company.add_an_employee()
            if selected_index == 6:
                company.remove_an_employee()
        except Exception as e:
            print(f"Error----------{e}-------------Error")
        
        company.save_records()

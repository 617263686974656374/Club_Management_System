import uuid

class Club:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.id = uuid.uuid4()

    def __str__(self):
        return f"\nID: {self.id}\nName: {self.name}\nSurname: {self.surname}"


class Employee(Club):
    def __init__(self, name, surname, job_position, ):
        super().__init__(name, surname)
        self.job_position = job_position

    def __str__(self):
        info = super().__str__()
        return f"\n{info}\nJob Position: {self.job_position}\n"


class Director(Club):
    def __init__(self, name, surname, age):
        super().__init__(name, surname)
        self.age = age
        self.managers_data = []

    def add_manager(self, manager_):
        if manager_ not in self.managers_data:
            self.managers_data.append(manager_)
            print(f"Manazer {manager_.name} pridaný do tímu riaditela {self.name}.")
        else:
            print("Manazer je uz priradeny")

    def update_manager(self, manager, directors):
        for director in directors:
            if manager in director.managers_data and director != self:
                director.managers_data.remove(manager)

        if manager not in self.managers_data:
            self.managers_data.append(manager)
            print(f"Manažér {manager.name} priradený riaditeľovi {self.name}.")
        else:
            print(f"Manažér {manager.name} už je v tíme riaditeľa {self.name}.")

    def __str__(self):
        info = super().__str__()
        return f"{info}\nAge: {self.age}\n"


class Owner(Club):
    total_stakes = 100

    def __init__(self, name, surname, stakes):
        super().__init__(name, surname)
        self.stakes = stakes

    def __str__(self):
        info = super().__str__()
        return f"{info}\nStakes: {self.stakes} %\n"


class Manager (Club):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.employees_data = []

    def add_employee(self, employee):
        if employee not in self.employees_data:
            self.employees_data.append(employee)
            print(f"Zamestnanec {employee.name} pridaný do tímu manažéra {self.name}.")
        else:
            print("Zamestnanec už je v tíme iného manažéra.")

    def update_employee(self, employee, managers):
        for manager in managers:
            if employee in manager.employees_data and manager != self:
                manager.employees_data.remove(employee)

        # Pridať zamestnanca do aktuálneho manažéra
        if employee not in self.employees_data:
            self.employees_data.append(employee)
            print(f"Zamestnanec {employee.name} priradený manažérovi {self.name}.")
        else:
            print(f"Zamestnanec {employee.name} už je v tíme manažéra {self.name}.")

    def __str__(self):
        return f"{len(self.employees_data)} : Employees in team\n"




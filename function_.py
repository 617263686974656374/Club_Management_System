
from Management_ import *
import tkinter as tk
management = Management()


def add_employee(name, surname, job_position):
    person = Employee(name, surname, job_position)
    management.add_person_to_management(person)
    save_to_csv()
    print("employee added: ", person.__str__())  # docasne overovanie
    for i in management.employees:  # docasne overovanie
        print("Zamestnanci ", i)  # docasne overovanie


def add_manager(name, surname):
    person = Manager(name, surname)
    management.add_person_to_management(person)
    save_to_csv()
    print("manager added", person.__str__())  # docasne overovanie
    for i in management.managers:  # docasne overovanie
        print(" Manazeri ", i)  # docasne overovanie


def add_director(name, surname, age):
    person = Director(name, surname, age)
    management.add_person_to_management(person)
    save_to_csv()
    print("director added", person.__str__())  # docasne overovanie
    for i in management.directors:  # docasne overovanie
        print(" Directors ", i)  # docasne overovanie


def add_owner(name, surname, stakes):
    person = Owner(name, surname, stakes)
    management.add_person_to_management(person)
    save_to_csv()
    print("owner added", person.__str__())  # docasne overovanie
    for i in management.owners:  # docasne overovanie
        print(" Owners ", i)  # docasne overovanie


def show_all(my_tree):
    my_tree.delete(*my_tree.get_children())
    for employee in management.employees:
        add_info = f"Job position: {employee.job_position}"
        my_tree.insert('', 'end', text='Employee', values=(employee.name, employee.surname, add_info, employee.id))
    for manager in management.managers:
        my_tree.insert('', 'end', text='Manager', values=(manager.name, manager.surname, manager.__str__(), manager.id))
    for director in management.directors:
        add_info = f"Age: {director.age}"
        my_tree.insert('', 'end', text='Director', values=(director.name, director.surname, add_info, director.id))
    for owner in management.owners:
        add_info = f"Total stakes: {owner.stakes}"
        my_tree.insert('', 'end', text='Owner', values=(owner.name, owner.surname, add_info, owner.id))


def find_person_by_id(person_id):
    print("Hľadané ID:", person_id, type(person_id))  # docasne overovanie
    for employee in management.employees:
        print("Zamestnanec ID:", employee.id, type(employee.id))  # docasne overovanie
        if str(employee.id) == person_id:
            return employee
    for manager in management.managers:
        print("Zamestnanec ID:", manager.id, type(manager.id))  # docasne overovanie
        if str(manager.id) == person_id:
            return manager
    for director in management.directors:
        if str(director.id) == person_id:
            return director
    for owner in management.owners:
        if str(owner.id) == person_id:
            return owner
    return None


def add_person(whoami, inputs, window, tree):
    if not inputs:
        print("Vyberte jednu z moznosti koho chcete pridat.")  # docasne overovanie
        messagebox.showwarning("Missing Data", "Please select one of function you want to add")
        return

    all_fields_filled = all(widget.get() for widget in inputs.values())
    if not all_fields_filled:
        messagebox.showwarning("Missing Data", "All fields must be filled")
        return

    try:
        data = {key: widget.get().title() if isinstance(widget, tk.Entry) else widget.get()
                for key, widget in inputs.items()}
        print("Zozbierané dáta:", data)  # docasne overovanie
        if whoami == 'Employee':
            add_employee(data['Name'], data['Surname'], data['Job position'])
            show_all(tree)
            window.destroy()
        elif whoami == 'Manager':
            add_manager(data['Name'], data['Surname'])
            show_all(tree)
            window.destroy()
        elif whoami == 'Director':
            add_director(data['Name'], data['Surname'], data['Age'])
            show_all(tree)
            window.destroy()
        elif whoami == 'Owner':
            stakes = int(data.get('Stakes', 0))
            add_owner(data['Name'], data['Surname'], stakes)
            show_all(tree)
            window.destroy()
    except AttributeError as e:
        print("Chyba pri získavaní dát: ", e)


def update_person(whoami, person_to_edit, inputs, my_tree, window):
    if not inputs:
        messagebox.showwarning("Warning", "No data to update.")
        return

    data = {key: widget.get() for key, widget in inputs.items()}
    print("Údaje na aktualizáciu:", data)  # docasne overovanie

    # Aktualizujeme všeobecné atribúty, ktoré sú spoločné pre všetky typy osôb
    if hasattr(person_to_edit, 'name'):
        person_to_edit.name = data.get('Name', '')
    if hasattr(person_to_edit, 'surname'):
        person_to_edit.surname = data.get('Surname', '')

    # Ďalej aktualizujeme špecifické atribúty podľa typu osoby
    if whoami == 'Employee':
        if hasattr(person_to_edit, 'job_position'):
            person_to_edit.job_position = data.get('Job position', '')
    elif whoami == 'Director':
        if hasattr(person_to_edit, 'age'):
            person_to_edit.age = data.get('Age', '')
    elif whoami == 'Owner':
        if hasattr(person_to_edit, 'stakes'):
            person_to_edit.stakes = data.get('Stakes', '')
    elif whoami == 'Manager':
        pass
    show_all(my_tree)
    window.destroy()
    save_to_csv()
    print(f"Osoba aktualizovaná: {person_to_edit}")  # docasne overovanie


def create_input_field(parent, label_text, row, validate_type, default_value=""):
    tk.Label(parent, text=label_text).grid(row=row, column=0)
    validation = (parent.register(validate_entry), '%P', validate_type)
    entry = tk.Entry(parent, validate="key", validatecommand=validation)
    entry.grid(row=row, column=1)
    entry.insert(0, default_value)
    return entry


def validate_entry(entry, whoami):
    if whoami == 'abc':
        if not (entry.isalpha() or entry == ""):
            messagebox.showwarning("Invalid Entry", "Please enter alphabet only")
            return False
    elif whoami == 'num':
        if not (entry.isdigit() or entry == ""):
            messagebox.showwarning("Invalid Entry", "Please enter numbers only")
            return False
    elif whoami == 'stake':
        if not entry:
            return True  # Povoliť prázdny vstup
        if not entry.isdigit():
            messagebox.showwarning("Invalid Entry", "Please enter numbers only")
            return False
        num = int(entry)
        max_allowed_stakes = Owner.total_stakes - management.total_stakes
        if not (0 < num <= max_allowed_stakes):
            messagebox.showwarning("Invalid Entry", f"Stakes must be between 1 and {max_allowed_stakes}")
            return False
    return True  # Ak nie je splnená žiadna z podmienok, považovať za platný vstup


def delete_person(my_tree):
    selected_item_tuple = my_tree.selection()
    if selected_item_tuple:
        selected_item = selected_item_tuple[0]
        selected_values = my_tree.item(selected_item, 'values')
        selected_id = selected_values[-1]

        person_to_delete = find_person_by_id(selected_id)
        if person_to_delete:
            management.remove_person(person_to_delete)
            my_tree.delete(selected_item)
            save_to_csv()
            print(f"Osoba {person_to_delete} bola odstránená.")
        else:
            messagebox.showwarning("Warning", "Osoba nenájdená.")
    else:
        messagebox.showwarning("No Selection", "Vyberte osobu na odstránenie.")


def update_manager(tree, select):
    selected_item = tree.selection()
    if selected_item:
        selected_name = select.get()
        selected_id = tree.item(selected_item[0], 'values')[4]
        selected_role = tree.item(selected_item[0], 'values')[2]
        print("Vybrané ID:", selected_id)

        if selected_role == "Employee":
            # Nájsť manažéra podľa mena
            selected_manager = next((manager for manager in management.managers if manager.name == selected_name), None)
            # Nájsť zamestnanca podľa ID
            selected_employee = find_person_by_id(selected_id)

            if selected_manager and selected_employee:
                selected_manager.update_employee(selected_employee, management.managers)
                save_to_csv()

        elif selected_role == "Manager":
            # Nájsť riaditeľa podľa mena
            selected_director = next((director for director in management.directors if director.name == selected_name),
                                     None)
            # Nájsť manažéra podľa ID
            selected_manager = find_person_by_id(selected_id)

            if selected_director and selected_manager:
                print(
                    f"Pôvodný počet manažérov riaditeľa {selected_director.name}: {len(selected_director.managers_data)}")  # Debugovací výpis
                selected_director.update_manager(selected_manager, management.directors)
                print(f"Manažér {selected_manager.name} priradený riaditeľovi {selected_director.name}.")
                print(
                    f"Nový počet manažérov riaditeľa {selected_director.name}: {len(selected_director.managers_data)}")  # Debugovací výpis
                save_to_csv()
                print(f"Riaditeľ {selected_director.name} priradený manažérovi {selected_manager.name}.")

        else:
            print("Osoba pre priradenie nebola nájdená.")

        refresh_management_tree(tree)


def refresh_management_tree(tree):
    tree.delete(*tree.get_children())
    for employee in management.employees:
        manager_name = find_manager_for_employee(employee, management.managers)
        tree.insert('', 'end', values=(employee.name, employee.surname, "Employee", manager_name, str(employee.id)))
    for manager in management.managers:
        director_name = find_director_for_manager(manager, management.directors)
        tree.insert('', 'end', values=(manager.name, manager.surname, "Manager", director_name, str(manager.id)))


def find_manager_for_employee(employee, managers):
    for manager in managers:
        if employee in manager.employees_data:
            return manager.name, manager.surname
    return "N/A"


def find_director_for_manager(manager, directors):
    for director in directors:
        if manager in director.managers_data:
            return director.name, manager.surname
    return "N/A"


def save_to_csv(filename="data.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'ID', 'Name', 'Surname', 'Additional Info', 'Associated IDs'])

        for employee in management.employees:
            writer.writerow(['Employee', employee.id, employee.name, employee.surname, employee.job_position, ''])

        for manager in management.managers:
            # Získanie ID zamestnancov priradených manažérovi
            employee_ids = [str(emp.id) for emp in manager.employees_data]
            writer.writerow(['Manager', manager.id, manager.name, manager.surname, '', '; '.join(employee_ids)])

        for director in management.directors:
            # Získanie ID manažérov priradených riaditeľovi
            manager_ids = [str(man.id) for man in director.managers_data]
            writer.writerow(['Director', director.id, director.name, director.surname, director.age, '; '.join(manager_ids)])

        for owner in management.owners:
            writer.writerow(['Owner', owner.id, owner.name, owner.surname, owner.stakes, ''])

    print(f"Údaje boli úspešne uložené do súboru '{filename}'.")


def load_from_csv(filename="data.csv"):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Preskočiť hlavičku

            # Pomocné kontajnery na dočasné uchovanie údajov
            temp_employees = {}
            temp_managers = {}
            temp_directors = {}
            manager_associated_ids = {}
            director_associated_ids = {}

            for row in reader:
                entity_type, entity_id, name, surname, additional_info, associated_ids = row

                # Vytvorenie objektov podľa typu a uloženie do dočasných kontajnerov
                if entity_type == 'Employee':
                    temp_employees[entity_id] = Employee(name, surname, additional_info)
                elif entity_type == 'Manager':
                    temp_managers[entity_id] = Manager(name, surname)
                    manager_associated_ids[entity_id] = associated_ids
                elif entity_type == 'Director':
                    temp_directors[entity_id] = Director(name, surname, additional_info)
                    director_associated_ids[entity_id] = associated_ids
                elif entity_type == 'Owner':
                    stakes = int(additional_info)
                    management.add_person_to_management(Owner(name, surname, stakes))

            # Priradenie zamestnancov manažérom
            for manager_id, manager in temp_managers.items():
                associated_employee_ids = manager_associated_ids.get(manager_id, '').split('; ')
                for employee_id in associated_employee_ids:
                    if employee_id in temp_employees:
                        manager.add_employee(temp_employees[employee_id])
                management.add_person_to_management(manager)

            # Priradenie manažérov riaditeľom
            for director_id, director in temp_directors.items():
                associated_manager_ids = director_associated_ids.get(director_id, '').split('; ')
                for manager_id in associated_manager_ids:
                    if manager_id in temp_managers:
                        director.add_manager(temp_managers[manager_id])
                management.add_person_to_management(director)

            # Pridanie manažérov, ktorí neboli priradení žiadnemu riaditeľovi
            for manager_id, manager in temp_managers.items():
                if not any(manager in director.managers_data for director in temp_directors.values()):
                    management.add_person_to_management(manager)

            # Adding employees who have not been assigned to any manager
            for employee_id, employee in temp_employees.items():
                management.add_person_to_management(employee)

        print(f"Údaje boli úspešne načítané zo súboru '{filename}'.")
    except FileNotFoundError:
        print("Save will be in folder Data.csv")

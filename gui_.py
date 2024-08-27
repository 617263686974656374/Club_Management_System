import tkinter as tk
from tkinter import ttk, messagebox
from function_ import *


def window_add_person_start():
    window_add_person = tk.Toplevel()
    window_add_person.title("Add Person")
    window_add_person.grab_set()

    tk.Label(window_add_person, text="Select function").grid(row=0, column=0)
    n = tk.StringVar()
    club_function = ttk.Combobox(window_add_person, width=20, textvariable=n, state='readonly')
    club_function['values'] = ('Employee', 'Director', 'Owner', 'Manager')
    club_function.grid(row=0, column=1)

    frame_inputs = tk.Frame(window_add_person)
    frame_inputs.grid(row=1, column=1)

    inputs = {}

    def update_fields(event, default_data=None):
        for widget in frame_inputs.winfo_children():
            widget.destroy()

        inputs.clear()
        fields = fields_mapping[club_function.get()]
        for i, (field_name, validate_type) in enumerate(fields.items()):
            default_value = default_data[field_name] if default_data and field_name in default_data else ""
            inputs[field_name] = create_input_field(frame_inputs, field_name, i, validate_type, default_value)

    fields_mapping = {
        'Employee': {"Name": "abc", "Surname": "abc", "Job position": "abc"},
        'Director': {"Name": "abc", "Surname": "abc", "Age": "num"},
        'Owner': {"Name": "abc", "Surname": "abc", "Stakes": "stake"},
        'Manager': {"Name": "abc", "Surname": "abc"}
    }

    club_function.bind('<<ComboboxSelected>>', update_fields)

    tk.Button(window_add_person, text="Add Person", command=lambda: add_person(club_function.get(), inputs, window_add_person, my_tree)).grid(row=2, column=1)

    window_add_person.mainloop()


def window_edit_person_start():
    selected_item = my_tree.selection()
    selected_item_tuple = my_tree.selection()
    if selected_item_tuple:
        selected_item = selected_item_tuple[0]
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a person to edit")
        return

    selected_values = my_tree.item(selected_item, 'values')
    selected_id = selected_values[-1]
    person_to_edit = find_person_by_id(selected_id)
    print("Found person:", person_to_edit)

    window_edit_person = tk.Toplevel()
    window_edit_person.title("Edit Person")
    window_edit_person.grab_set()

    frame_inputs = tk.Frame(window_edit_person)
    frame_inputs.grid(row=1, column=1)

    tk.Label(window_edit_person, text="Select function").grid(row=0, column=0)
    n = tk.StringVar()
    club_function = ttk.Combobox(window_edit_person, width=20, textvariable=n, state='readonly')
    club_function['values'] = ('Employee', 'Director', 'Owner', 'Manager')
    club_function.grid(row=0, column=1)
    inputs = {}

    def update_fields(event, person=None):
        for widget in frame_inputs.winfo_children():
            widget.destroy()
        selected_function = n.get()
        if selected_function in fields_mapping:
            fields = fields_mapping[selected_function]
            for i, (field_name, validate_type) in enumerate(fields.items()):
                default_value = ""
                if person:
                    attribute_name = field_name.lower().replace(" ", "_")
                    if hasattr(person, attribute_name):
                        default_value = getattr(person, attribute_name, "")
                        print(f"Aktualizácia poľa {field_name} s hodnotou: {default_value}")
                    else:
                        print(f"Osoba nemá atribút {attribute_name}, vstup bude prázdny.")

                inputs[field_name] = create_input_field(frame_inputs, field_name, i, validate_type, default_value)

    fields_mapping = {
        'Employee': {"Name": "abc", "Surname": "abc", "Job position": "abc"},
        'Director': {"Name": "abc", "Surname": "abc", "Age": "num"},
        'Owner': {"Name": "abc", "Surname": "abc", "Stakes": "stake"},
        'Manager': {"Name": "abc", "Surname": "abc"}
    }

    if person_to_edit:
        person_type = type(person_to_edit).__name__
        club_function.set(person_type)
        club_function.config(state='disabled')
        if person_type in fields_mapping:
            update_fields(None, person_to_edit)
        else:
            messagebox.showwarning("Warning", "Unknown person type.")
    else:
        messagebox.showwarning("Warning", "Person not found.")

    club_function.bind('<<ComboboxSelected>>', lambda event: update_fields(event, person_to_edit))

    tk.Button(window_edit_person, text="Update Person", command=lambda: update_person(club_function.get(), person_to_edit, inputs, my_tree, window_edit_person)).grid(row=2, column=1)

    window_edit_person.mainloop()


def open_management_window():
    management_window = tk.Toplevel()
    management_window.title("Management")
    management_window.grab_set()

    management_tree = ttk.Treeview(management_window)
    management_tree.grid(row=0, column=0, columnspan=2, sticky='nesw')

    management_tree["columns"] = ("Name", "Surname", "Role", "Superior", "ID")
    for col in management_tree["columns"]:
        management_tree.heading(col, text=col)
        management_tree.column(col, anchor="center", width=200)
    management_tree.column("#0", width=5, anchor="center")
    management_tree.column("ID", width=0, stretch=False)
    for employee in management.employees:
        manager_name = find_manager_for_employee(employee, management.managers)
        management_tree.insert('', 'end', values=(employee.name, employee.surname, "Employee", manager_name, str(employee.id)))
    for manager in management.managers:
        director_name = find_director_for_manager(manager, management.directors)
        management_tree.insert('', 'end', values=(manager.name, manager.surname, "Manager", director_name, str(manager.id)))

    # Combobox na výber manažéra alebo riaditeľa
    select_label = tk.Label(management_window, text="")
    select_label.grid(row=1, column=0, sticky='e')
    select_combo = ttk.Combobox(management_window, state="readonly")
    select_combo.grid(row=1, column=1)
    select_label.grid_remove()
    select_combo.grid_remove()

    def on_tree_select(event):
        selected_item = management_tree.selection()
        if selected_item:
            selected_role = management_tree.item(selected_item[0], 'values')[2]
            update_select_combo(selected_role)
        else:
            select_label.grid_remove()
            select_combo.grid_remove()

    def update_select_combo(role):
        if role == "Employee":
            select_label.config(text="Select Manager:")
            select_combo['values'] = [manager.name for manager in management.managers], [manager.surname for manager in management.managers]
            select_label.grid()
            select_combo.grid()
        elif role == "Manager":
            select_label.config(text="Select Director:")
            select_combo['values'] = [director.name for director in management.directors], [director.surname for director in management.directors]
            select_label.grid()
            select_combo.grid()
        else:
            select_label.grid_remove()
            select_combo.grid_remove()

    management_tree.bind("<<TreeviewSelect>>", on_tree_select)

    btn_update_manager = tk.Button(management_window, text="Update Manager", command=lambda: update_manager(management_tree, select_combo))

    btn_update_manager.grid(row=1, column=2)


# ********************************************** Main menu ********************************************************


window_main_menu = tk.Tk()
window_main_menu.title("Club management")


my_tree = ttk.Treeview(window_main_menu)
my_tree.grid(row=0, column=0, columnspan=4, sticky='nesw')

my_tree["columns"] = ("Name", "Surname", "Add info", "ID")
my_tree.column("ID", width=0, stretch=False)
my_tree.heading("#0", text="Function", anchor="w")
my_tree.column("#0", anchor="w", width=40)
my_tree.heading("Name", text="Name")
my_tree.column("Name", width=40)
my_tree.heading("Surname", text="Surname")
my_tree.column("Surname", width=40)
my_tree.heading("Add info", text="Add info")
my_tree.column("Add info", anchor="center", width=80)

show_all(my_tree)

btn_add_person = tk.Button(window_main_menu, text="Add Person", width=60, command=lambda: window_add_person_start())
btn_add_person.grid(row=1, column=0)

btn_edit_person = tk.Button(window_main_menu, text="Edit Person", width=60, command=window_edit_person_start)
btn_edit_person.grid(row=2, column=0)

btn_delete_person = tk.Button(window_main_menu, text="Delete Person", width=60, command=lambda: delete_person(my_tree))
btn_delete_person.grid(row=3, column=0)

btn_management = tk.Button(window_main_menu, text="Management", width=60, command=lambda: open_management_window())
btn_management.grid(row=4, column=0)


def start():
    load_from_csv()
    show_all(my_tree)
    window_main_menu.mainloop()


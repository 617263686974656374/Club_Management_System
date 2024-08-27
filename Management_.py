import csv

from Club_ import *
from tkinter import messagebox


class Management:
    def __init__(self):
        self.employees = []
        self.directors = []
        self.owners = []
        self.managers = []
        self.total_stakes = 0
        #self.manag = Manager

    def add_person_to_management(self, person):
        if isinstance(person, Employee):
            self.employees.append(person)
        elif isinstance(person, Director):
            self.directors.append(person)
        elif isinstance(person, Owner):
            self.owners.append(person)
            self.update_total_stakes()
        elif isinstance(person, Manager):
            self.managers.append(person)
        return True

    def remove_person(self, person):
        if person in self.employees:
            self.employees.remove(person)
        elif person in self.directors:
            self.directors.remove(person)
        elif person in self.owners:
            self.owners.remove(person)
        elif person in self.managers:
            self.managers.remove(person)

    def update_total_stakes(self):
        self.total_stakes = sum(owner.stakes for owner in self.owners)


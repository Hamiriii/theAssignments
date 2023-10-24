import json
import re
import tkinter as tk
from tkinter import ttk, messagebox

class ContactManager:
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    PHONE_REGEX = re.compile(r"\d{10}")

    @classmethod
    def validate_input(cls, email, phone):
        return cls.EMAIL_REGEX.fullmatch(email) and cls.PHONE_REGEX.fullmatch(phone)

    @staticmethod
    def load_contacts(file='contacts.json'):
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    @staticmethod
    def save_contacts(contacts, file='contacts.json'):
        with open(file, 'w') as f:
            json.dump(contacts, f)

    def __init__(self, root):
        self.contacts = self.load_contacts()
        self.root = root
        self.init_gui()

    def init_gui(self):
        self.tabControl = ttk.Notebook(self.root)
        tabs = ['Add', 'Search', 'Delete', 'List', 'Update']
        for tab in tabs:
            frame = ttk.Frame(self.tabControl)
            self.tabControl.add(frame, text=tab)
            getattr(self, f'init_{tab.lower()}')(frame)
        self.tabControl.pack(expand=1, fill="both")
        self.status_bar = ttk.Label(self.root, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_labeled_entries(self, frame, labels):
        return {label: self.create_labeled_entry(frame, label) for label in labels}

    @staticmethod
    def create_labeled_entry(frame, label):
        ttk.Label(frame, text=f"{label}:").pack()
        entry = ttk.Entry(frame)
        entry.pack()
        return entry

    def update_status(self, message):
        self.status_bar.config(text=message)

    def init_add(self, frame):
        self.add_entries = self.create_labeled_entries(frame, ['Name', 'Email', 'Phone'])
        ttk.Button(frame, text="Add Contact", command=self.add_contact).pack()

    def add_contact(self):
        entries = {key: entry.get() for key, entry in self.add_entries.items()}
        if self.validate_input(entries['Email'], entries['Phone']):
            self.contacts.append(entries)
            self.save_contacts(self.contacts)
            self.update_status("Contact added.")
        else:
            messagebox.showerror("Invalid Input", "Valid email and 10-digit phone number required.")

    def init_search(self, frame):
        self.search_entries = self.create_labeled_entries(frame, ['Name'])
        ttk.Button(frame, text="Search", command=self.search_contact).pack()

    def search_contact(self):
        name = self.search_entries['Name'].get()
        for contact in self.contacts:
            if contact['Name'] == name:
                messagebox.showinfo("Found", f"Name: {contact['Name']}\nEmail: {contact['Email']}\nPhone: {contact['Phone']}")
                return
        self.update_status("Contact not found.")

    def init_delete(self, frame):
        self.delete_entries = self.create_labeled_entries(frame, ['Name'])
        ttk.Button(frame, text="Delete", command=self.delete_contact).pack()

    def delete_contact(self):
        name = self.delete_entries['Name'].get()
        for i, contact in enumerate(self.contacts):
            if contact['Name'] == name:
                del self.contacts[i]
                self.save_contacts(self.contacts)
                self.update_status("Contact deleted.")
                return
        self.update_status("Contact not found.")

    def init_list(self, frame):
        ttk.Button(frame, text="List All Contacts", command=self.list_contacts).pack()

    def list_contacts(self):
        list_text = ""
        for contact in self.contacts:
            list_text += f"Name: {contact['Name']}, Email: {contact['Email']}, Phone: {contact['Phone']}\n"
        if list_text:
            messagebox.showinfo("Contact List", list_text)
        else:
            self.update_status("No contacts available.")

    def init_update(self, frame):
        self.update_entries = self.create_labeled_entries(frame, ['Name', 'New Email', 'New Phone'])
        ttk.Button(frame, text="Update", command=self.update_contact).pack()

    def update_contact(self):
        name = self.update_entries['Name'].get()
        new_email = self.update_entries['New Email'].get()
        new_phone = self.update_entries['New Phone'].get()
        for contact in self.contacts:
            if contact['Name'] == name:
                if new_email:
                    contact['Email'] = new_email
                if new_phone:
                    contact['Phone'] = new_phone
                self.save_contacts(self.contacts)
                self.update_status("Contact updated.")
                return
        self.update_status("Contact not found.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sophisticated Contact Manager")
    root.geometry("450x400")
    app = ContactManager(root)
    root.mainloop()

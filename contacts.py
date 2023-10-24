import json
import re
import tkinter as tk
from tkinter import ttk, messagebox

def load_contacts():
    try:
        with open('contacts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_contacts(contacts):
    with open('contacts.json', 'w') as f:
        json.dump(contacts, f)

def add_contact():
    name = name_entry.get()
    num = number_entry.get()
    email = email_entry.get()
    if not re.fullmatch(r"\d{10}", num) or not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email):
        messagebox.showerror("Invalid Input", "Valid email and 10-digit phone number required.")
        return
    new_contact = {'name': name, 'number': num, 'email': email}
    contacts.append(new_contact)
    save_contacts(contacts)
    status_bar.config(text="Contact added.")

def search_contact():
    search_name = search_entry.get()
    for contact in contacts:
        if contact['name'] == search_name:
            messagebox.showinfo("Found", f"Name: {contact['name']}\nNumber: {contact['number']}\nEmail: {contact['email']}")
            return
    status_bar.config(text="Contact not found.")

def delete_contact():
    del_name = delete_entry.get()
    for i, contact in enumerate(contacts):
        if contact['name'] == del_name:
            del contacts[i]
            save_contacts(contacts)
            status_bar.config(text="Contact deleted.")
            return
    status_bar.config(text="Contact not found.")

def list_contacts():
    list_text = ""
    for contact in contacts:
        list_text += f"Name: {contact['name']}, Number: {contact['number']}, Email: {contact['email']}\n"
    if list_text:
        messagebox.showinfo("Contact List", list_text)
    else:
        status_bar.config(text="No contacts available.")

def update_contact():
    update_name = update_entry.get()
    for i, contact in enumerate(contacts):
        if contact['name'] == update_name:
            new_number = update_number_entry.get()
            new_email = update_email_entry.get()
            if new_number:
                contacts[i]['number'] = new_number
            if new_email:
                contacts[i]['email'] = new_email
            save_contacts(contacts)
            status_bar.config(text="Contact updated.")
            return
    status_bar.config(text="Contact not found.")

contacts = load_contacts()

root = tk.Tk()
root.title("Enhanced Contact Manager")
root.geometry("450x400")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text="Add")
tabControl.add(tab2, text="Search")
tabControl.add(tab3, text="Delete")
tabControl.add(tab4, text="List")
tabControl.add(tab5, text="Update")

tabControl.pack(expand=1, fill="both")

# Add Contact
ttk.Label(tab1, text="Name:").pack()
name_entry = ttk.Entry(tab1)
name_entry.pack()

ttk.Label(tab1, text="Number:").pack()
number_entry = ttk.Entry(tab1)
number_entry.pack()

ttk.Label(tab1, text="Email:").pack()
email_entry = ttk.Entry(tab1)
email_entry.pack()

ttk.Button(tab1, text="Add Contact", command=add_contact).pack()

# Search Contact
ttk.Label(tab2, text="Name:").pack()
search_entry = ttk.Entry(tab2)
search_entry.pack()
ttk.Button(tab2, text="Search", command=search_contact).pack()

# Delete Contact
ttk.Label(tab3, text="Name:").pack()
delete_entry = ttk.Entry(tab3)
delete_entry.pack()
ttk.Button(tab3, text="Delete", command=delete_contact).pack()

# List Contacts
ttk.Button(tab4, text="List All Contacts", command=list_contacts).pack()

# Update Contact
ttk.Label(tab5, text="Name:").pack()
update_entry = ttk.Entry(tab5)
update_entry.pack()

ttk.Label(tab5, text="New Number:").pack()
update_number_entry = ttk.Entry(tab5)
update_number_entry.pack()

ttk.Label(tab5, text="New Email:").pack()
update_email_entry = ttk.Entry(tab5)
update_email_entry.pack()

ttk.Button(tab5, text="Update", command=update_contact).pack()

# Status Bar
status_bar = ttk.Label(root, text="", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()

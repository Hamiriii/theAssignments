import json
import re

def contact():
    contacts = []  
    while True:
        try:
            name = input("Enter the contact's name: ")
            num = input("Enter number: ")
            if not num.isdigit() or len(num) != 10:
                raise ValueError("Enter a valid phone number")

            email = input("Enter email: ")
            if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email):
                raise ValueError("Make sure you enter a valid email.")

            new_contact = {'name': name, 'number': num, 'email': email}
            contacts.append(new_contact) 
            print("Contact added successfully!")

            with open('contacts.json', 'w') as f:
                json.dump(contacts, f) 

            break  

        except ValueError as ve:
            print(ve)  

        except:
            print("Oops, something went wrong. Let's try again.")
            continue 

def main():
    contact()

if __name__ == "__main__":
    main()

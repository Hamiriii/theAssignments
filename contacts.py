import json

def contact():
    try:
        name = input("Enter the contacts name: ")
        while True:
            try: 
                num = int(input("Enter number: "))
                if isinstance(num, int) or len(num) > 10 or len(num) < 10:
                    raise ValueError, "Enter a valid phone number"
            except ValueError:
                num = int(input("Enter number: "))
            try:   
                email = input("Enter email: ")
                




    
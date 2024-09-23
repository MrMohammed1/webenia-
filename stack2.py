import csv
import re

class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email



class ContactManager:
    def __init__(self, filename):
        self.filename = filename
        self.contacts = self.contacts()
        self.last_action = None
        self.last_deleted_contact = None

    def contacts(self):
        contacts = []
        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for i in reader:
                    contacts.append(i)
        except FileNotFoundError:
            pass
        return contacts

    def save(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['name', 'phone', 'email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.contacts)

    def add(self):
        name = input("enter name: ")
        
        while True:
            phone = input("enter phone number: ")
            if re.match(r"^(010|011|012|015)\d{8}$", phone):
                break
            else:
                print("invalid phone number")
                choice = input("type '1' to try again or '2' to see options: ")
                if choice == '2':
                    return 
        
        while True:
            email = input("enter email: ")
            if re.match(r"^[A-z0-9\.]+@[A-z0-9]+\.(com|net|org|info)$", email):
                break
            else:
                print("invalid email")
                choice = input("write '1' to retry or '2' to see options: ")
                if choice == '2':
                    return  
        
        new_contact = {'name': name, 'phone': phone, 'email': email}
        self.contacts.append(new_contact)
        self.save()
        self.last_action = ("add", new_contact)
        print(f"Contact {name} added successfully!")

    def search(self, name):
        contacts = [i for i in self.contacts if name.lower() in i['name'].lower()]
        if contacts:
            for i in contacts:
                print(f"founde: {i}")
        else:
            print("contact not found.")

    def update(self, name):
        for i in self.contacts:
            if i['name'].lower() == name.lower():
                old_contact = i.copy()
                
                phone = input("enter new phone : ")
                if phone and not re.match(r"^(010|011|012|015)\d{8}$", phone):
                    print("invalid phone numberr")
                    return
                
                email = input("enter new emaill : ")
                if email and not re.match(r"[A-z0-9\.]+@[A-z0-9]+\.(com|net|org|info)$", email):
                    print("invalid email")
                    return
                
                if phone:
                    i['phone'] = phone
                if email:
                    i['email'] = email
                self.save()
                self.last_action = ("update", old_contact)
                print(f" {name} updated successfully!")
                return
        print("Contact not found.")

    def delete(self, name):
        for i in self.contacts:
            if i['name'].lower() == name.lower():
                self.contacts.remove(i)
                self.save()
                self.last_deleted_contact = i
                self.last_action = ("delete", i)
                print(f"Contact {name} deleted successfully!")
                return
        print("Contact not found.")

    def undo(self):
        if not self.last_action:
            print("Nothing to undo.")
            return

        action, contact = self.last_action
        if action == "add":
            self.contacts.remove(contact)
            print(f"{contact['name']} wasremoved")
        elif action == "delete":
            self.contacts.append(self.last_deleted_contact)
            print(f" {contact['name']} restored")
        elif action == "update":
            for j in self.contacts:
                if j['name'] == contact['name']:
                    j.update(contact)
                    print(f" {contact['name']} restored to it's previous ")
                    break
        self.save()
        self.last_action = None

    def view_all_contacts(self):
        if not self.contacts:
            print("No contacts found.")
        else:
            for contact in sorted(self.contacts, key=lambda x: x['name']):
                print(contact)

def running():
    manager = ContactManager('contacts.csv')

    while True:
        print("1. add the contact")
        print("2.search contact")
        print("3. update the contact")
        print("4. delete Contact")
        print("5.view all contacts")
        print("6. undo the action")
        print("7. exit")

        choice = input("enter choice: ")

        if choice == '1':
            manager.add()
        elif choice == '2':
            name = input("enter name to search: ")
            manager.search(name)
        elif choice == '3':
            name = input("enter name to update: ")
            manager.update(name)
        elif choice == '4':
            name = input("enter name to delete: ")
            manager.delete(name)
        elif choice == '5':
            manager.view_all_contacts()
        elif choice == '6':
            manager.undo()
        elif choice == '7':
            break
        else:
            print("invalid choice, try again.")

if __name__ == "__main__":
    running()


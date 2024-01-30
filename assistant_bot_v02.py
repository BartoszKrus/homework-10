from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        phone_to_remove = str(phone)
        if phone_to_remove in [str(p) for p in self.phones]:
            self.phones = [p for p in self.phones if str(p) != phone_to_remove]

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = Phone(old_phone)
        for i, phone in enumerate(self.phones):
            if str(phone) == str(old_phone_obj):
                self.phones[i] = Phone(new_phone)
                return
        print("Old phone number not found.")

    def __str__(self):
        return f"Name: {self.name}, Phones: {', '.join(map(str, self.phones))}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
      
    def find_records(self, keyword):
        results = []
        keyword_lower = keyword.lower()
        for record in self.data.values():
            if keyword_lower == record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if keyword_lower == str(phone).lower():
                        results.append(record)
                        break  
        return results
    
    def phone_exists(self, name, phone):
        existing_records = self.find_records(name)
        if existing_records:
            record = existing_records[0]
            return str(phone) in [str(phone_obj) for phone_obj in record.phones]
        return False
    
    
def main():
    """
    The main() function is responsible for managing user interaction with the phone book.
    Users can perform various operations on entries in the phone book, such as adding,
    editing, removing, searching, and displaying entries.

    Commands:
    - '.' - end the program.
    - 'good bye', 'close', 'exit' - end the program with the message "Good bye!".
    - 'hello' - display a greeting.
    - 'add' - add a new entry to the phone book.
    - 'add phone' - add a new phone number to an existing entry.
    - 'edit phone' - edit an existing phone number.
    - 'remove phone' - remove a phone number from an existing entry.
    - 'find' - search for entries in the phone book.
    - 'show all' - display all entries in the phone book.

    """
    address_book = AddressBook()

    while True:
        command = input("Enter command: ").lower()


        if '.' in command:
            break


        elif command in ['good bye', 'close', 'exit']:
            print("Good bye!")
            break


        elif command == "hello":
            print("How can I help you?")


        elif command == "add":
            name = input("Enter name: ")
            if not name.strip():
                print("Error: Name cannot be empty.\n")
                continue
                        
            existing_records = address_book.find_records(name)
            if existing_records:
                print(f"Error: This name: {name} already exists in the address book. Please choose a different name.\n")
                continue

            else:
                record = Record(name)                
                phone = input("Enter phone number: ")
                if phone.strip():
                    record.add_phone(Phone(phone))                
                address_book.add_record(record)
                print(f"Success: Record: {name}: {phone} added successfully.\n")


        elif command == "add phone":
            name = input("Enter name phone: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue
            
            existing_records = address_book.find_records(name)
            if not existing_records:
                print(f"Error: This name: {name} does not exist in the address book. Please add a new record first.\n")
            else:
                phone = input("Enter phone number: ")
                if phone.strip():
                    record = existing_records[0]
                    record.add_phone(Phone(phone))
                    print(f"Success: Phone number: {phone} added successfully to {name}.\n")
                else:
                    print("Error: No phone number was provided. No new number added.\n")


        elif command == "edit phone":
            name = input("Enter name to edit phone number: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue

            results = address_book.find_records(name)
            if results:
                record = results[0]
                phone = input("Enter new phone number: ")
                if phone.strip():
                    old_phone = input("Enter old phone number to replace: ")
                    if str(old_phone) in [str(phone_obj) for phone_obj in record.phones]:
                        record.edit_phone(Phone(old_phone), Phone(phone))
                        print(f"Success: Phone number: {phone} updated successfully.\n")
                    else:
                        print(f"Error: Old phone number: {old_phone} not found for {name}.\n")
                else:
                    print(f"Error: New phone number not provided.\n")                    
            else:
                print(f"Error: Name: {name} not found in the address book.\n")


        elif command == "remove phone":
            name = input("Enter name to remove phone number: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue

            existing_records = address_book.find_records(name)
            if existing_records:
                record = existing_records[0]
                phone = input("Enter phone number to remove: ")
                if str(phone) in [str(phone_obj) for phone_obj in record.phones]:
                    record.remove_phone(Phone(phone))
                    print(f"Success: Phone number: {phone} removed successfully.\n")
                else:
                    print(f"Error: Phone number: {phone} not found for {name}.\n")
            else:
                print(f"Error: Name: {name} not found in the address book.\n")


        elif command == "find":
            name = input("Enter name to search: ").strip()
            phone = input("Enter phone number to search: ").strip()
            if not name.strip() and not phone.strip():
                print("Error: Name and phone number cannot be empty.\n")
                continue

            results = []
            if name and phone:
                for record in address_book.values():
                    if name.lower() == record.name.value.lower() and phone in [str(p) for p in record.phones]:
                        results.append(record)
            elif name:
                for record in address_book.values():
                    if name.lower() == record.name.value.lower():
                        results.append(record)
            elif phone:
                for record in address_book.values():
                    if phone in [str(p) for p in record.phones]:
                        results.append(record)
            if results:
                print("Success: Matching records:")
                for record in results:
                    print(record)
            else:
                print("Error: No matching records found.")


        elif command == "show all":
            if address_book:
                print("Success: All Contacts:")
                for record in address_book.values():
                    print(record)
                print()
            else:
                print("Error: Address book is empty.\n")


        else:
            print("Error: Invalid command. Enter the correct command.\n")


if __name__ == "__main__":
    main()
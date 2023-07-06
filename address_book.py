from collections import UserDict
from datetime import datetime
from pickle import dump, load
from re import search

class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Name(Field):
    pass

class Address(Field):
    pass

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        new_value = (
            value.removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if len(new_value) in [10, 12] and new_value.isdigit():
            self._value = new_value
        else:
            raise ValueError
        
class Email(Field):
    @Field.value.setter
    def value(self, value):
        new_value = search(r"[a-zA-Z0-9_.]+@[a-zA-Z]+[.][a-zA-Z]{2,}", value)
        if new_value:
            self._value = new_value.group()
        else:
            raise ValueError("Invalid email.")
        
class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            self._value = value
        except ValueError:
            print("Invalid birthday format. Please use DD.MM.YYYY")

class Record:
    def __init__(self, name: Name, phone: Phone = None, address: Address = None, email: Email = None, birthday: Birthday = None):
        self.name = name
        self.phones = [phone]
        self.address = address
        self.email = email
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        for i, number in enumerate(self.phones):
            if phone == number:
                self.phones.pop(i)

    def change_phone_num(self, old_phone, new_phone):
        for i, number in enumerate(self.phones):
            if old_phone == number:
                self.phones[i] = new_phone

class AddressBook(UserDict):
    def add_record(self, record):
        self.data.update({record.name.value: record})

def main():
    try:
        with open("data.bin", "rb") as fh:
            ab = load(fh)
    except FileNotFoundError:
        ab = AddressBook()

    print("please write 'info' to get instructson about adressbook comands")

    while True:
        string = input('Enter command to AddressBook: ').lower()
        if string in ["good bye", "close", "exit"]:
            with open("data.bin", "wb") as fh:
                dump(ab, fh)
            print("You went to Personal Helper")
            break

        elif string == "info":
            print("Enter 'add (name) (phone)' to add contact's name and phone")
            print("Enter 'show all' to show all contacts in Address Book")

        elif string == "show all":
            for rec in ab.data.values():
                print(rec.name.value, [x.value for x in rec.phones])

        elif string.startswith("add"):
            parser = string.split(" ")
            name = Name(parser[1].capitalize())

            try:
                phone = Phone(parser[2])
            except ValueError:
                print("Invalid phone number. It contain only 10 or 12 digits.")

            try:
                if name.value not in ab.data:
                    record = Record(name, phone)
                    ab.add_record(record)
                else:
                    ab[name.value].add_phone(phone)
            except UnboundLocalError:
                pass

if __name__ == "__main__":
    main()
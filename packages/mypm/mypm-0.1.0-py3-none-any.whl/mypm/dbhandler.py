import shelve
import pyperclip
from .itemclass import Item


def add_item(name, args):
    with shelve.open("vault.db") as db:
        if name in db:
            print(
                f"Item already exists,\n{name}[{db[name].id}({'':*>{len(db[name].password)}})]")
        else:
            id = input("Enter the id: ",)
            while (not id):
                id = input("Enter the id: ")
            password = input("Enter the password: ")
            while (not password):
                password = input("Enter the password: ")
            db[name] = Item(id, password)
            print(
                f'''Item added\n{name:-<20}> {db[name].id}({'':*>{len(db[name].password)}})''')


def delete_item(name):
    with shelve.open("vault.db") as db:
        if name in db:
            del db[name]
            print("Item deleted")
        else:
            print("Item not found")


def update_item(name):
    with shelve.open("vault.db") as db:
        if name in db:
            x = input(f"Enter the id : {db[name].id} -> ")
            if x != "":
                id = x
            password = input("Enter the password: ")
            db[name] = Item(id, password)
            print(f"Item updated")
            print(
                f"{name:-<20}> {db[name].id}({'':*>{len(db[name].password)}})")
        else:
            print("Item not found")


def copy_item(name):
    with shelve.open("vault.db") as db:
        if name in db:
            pyperclip.copy(db[name].password)
            print("copied")
        else:
            print("Item not found")


def show_item(name):
    with shelve.open("vault.db") as db:
        if name in db:
            print(
                f"{name:-<20}> {db[name].id}({'':*>{len(db[name].password)}})")
        else:
            print("Item not found")


def list_items():
    with shelve.open("vault.db") as db:
        if not db.keys():
            print("No items found")
        for key in db.keys():
            print(f"{key:-<20}> {db[key].id}({'':*>{len(db[key].password)}})")


def clean():
    with shelve.open("vault.db") as db:
        for key in db.keys():
            del db[key]


if __name__ == "__main__":
    clean()

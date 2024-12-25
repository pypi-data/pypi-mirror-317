from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("Item", help="Name of the item",
                    action="store", type=str, nargs="?", default="")

parser.add_argument("-a", "--add", help="add item to vault",
                    action="store_true")

parser.add_argument("-d", "--delete", help="delete item from vault",
                    action="store_true")

parser.add_argument("-u", "--update", help="update item in vault",
                    action="store_true")

parser.add_argument("-l", "--list", help="list items in vault",
                    action="store_true")

parser.add_argument("-c", "--copy", help="search item in vault",
                    action="store_true")

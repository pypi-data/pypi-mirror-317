

class OptionObject:

    def __init__(self, args):
        self.ItemName = args.Item
        self.add = args.add
        self.delete = args.delete
        self.update = args.update
        self.copy = args.copy
        self.list = args.list

    def getExceptionString(self):
        if self.ItemName == "" and any([self.add, self.delete, self.update, self.copy]):
            return "Item name is required for ( add | delete | update | copy )"
        if self.add and any([self.delete, self.update, self.list]):
            return "Cannot use add with ( delete | update | list ) at the same time"
        if self.delete and any([self.add, self.update, self.copy, self.list]):
            return "Cannot use delete with ( add | update | copy | list ) at the same time"
        if self.update and any([self.add, self.delete, self.list]):
            return "Cannot update with ( add | delete | copy | list ) at the same time"
        if self.list and any([self.add, self.delete, self.update, self.copy, self.ItemName != ""]):
            return "Cannot list with ( item Name | add | delete | update | copy ) at the same time"

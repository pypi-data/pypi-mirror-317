from mypm import *


def main():

    args = parser.parse_args()

    if (ErrorString := OptionObject(args).getExceptionString()):
        print(ErrorString)
        exit()

    if args.Item != "":
        if args.add:
            add_item(args.Item, args)
        elif args.update:
            update_item(args.Item)

        if args.copy:
            copy_item(args.Item)
        if args.delete:
            delete_item(args.Item)

        if not any([args.add, args.update, args.copy, args.delete, args.list]):
            show_item(args.Item)
    else:
        if args.list:
            list_items()


# clean()
if __name__ == "__main__":
    main()

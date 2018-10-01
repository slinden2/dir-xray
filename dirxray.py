import os
import json
import dirxrayhelper


class Config:

    FILE = "dirxray_config.json"
    LINE_SEP = "=" * 30


def menu():
    print("""
DIR XRAY
DIRECTORY/FILE COMPARISON TOOL
====================================
Please type a number and press enter:

1.  Create an xray
2.  List xray files
3.  Compare xray files
4.  Set a new directory for xray files
5.  Info
6.  Exit
    """)

    user_input = dirxrayhelper.get_user_input(7)

    return user_input


if __name__ == "__main__":

    if not os.path.exists(os.path.join(os.getcwd(), Config.FILE)):
        config_dict = {}
        config_dict['save_to_xray_path'] = True
        config_dict['save_path'] = os.getcwd()
        try:
            with open(Config.FILE, 'w') as f:
                json.dump(config_dict, f, indent=4)
        except:
            print("Unable to create an initial config file.")
            input("Press [Enter] to exit.")
            exit()
        else:
            print(f"Config file created to the path:\
            {os.path.join(os.getcwd(), Config.FILE)}.")
            print()

    user_input = menu()
    archive_path = os.getcwd()

    while user_input != 6:
        if user_input == 1:
            os.system('cls')
            print("CREATE XRAY")
            print(Config.LINE_SEP)
            path = input("Enter a path: ")
            dirxrayhelper.create_xray(path)
            user_input = menu()

        elif user_input == 2:
            os.system('cls')
            print("LIST OF XRAY FILES")
            print(Config.LINE_SEP)
            dirxrayhelper.list_xrays()
            user_input = menu()

        elif user_input == 3:
            os.system('cls')
            print("COMPARE XRAY FILES")
            print(Config.LINE_SEP)
            dirxrayhelper.compare_xrays()
            user_input = menu()

        elif user_input == 4:
            os.system('cls')
            print("SET NEW DIRECTORY FOR THE XRAY FILES")
            print(Config.LINE_SEP)
            dirxrayhelper.set_file_directory()
            user_input = menu()

        elif user_input == 5:
            os.system('cls')
            print("INFO")
            print(Config.LINE_SEP)
            dirxrayhelper.info()
            user_input = menu()

    print("Thank you for using Dir XRAY.")

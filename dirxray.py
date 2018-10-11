import os
import json
import dirxrayhelper


class Config:
    FILE = "dirxray_config.json"
    LINE_SEP = "=" * 30
    EXIT_NUMBER = 9
    ENTER_CONTINUE = "Press <Enter> to continue."
    TITLE = f"""
DIR XRAY
DIRECTORY/FILE COMPARISON TOOL
{LINE_SEP}"""
    EXIT_ACTION = f"{EXIT_NUMBER}.  Exit"
    INDENT = "    "


class Controller:
    """Main controller class of the application. Generates the main
    menu.
    """
    @staticmethod
    def execute(user_input):
        controller_name = f"do_{user_input}"
        try:
            controller = getattr(Controller, controller_name)
        except AttributeError:
            pass
        else:
            controller()

    @staticmethod
    def do_1():
        """Create an xray"""
        os.system('cls')
        print("CREATE XRAY")
        print(Config.LINE_SEP)
        path = input("Enter a path: ")
        dirxrayhelper.create_xray(path)

    @staticmethod
    def do_2():
        """List xray files"""
        os.system('cls')
        print("LIST OF XRAY FILES")
        print(Config.LINE_SEP)
        dirxrayhelper.list_xrays()

    @staticmethod
    def do_3():
        """Compare xray files"""
        os.system('cls')
        print("COMPARE XRAY FILES")
        print(Config.LINE_SEP)
        dirxrayhelper.compare_xrays()

    @staticmethod
    def do_4():
        """Set a new directory for xray files"""
        os.system('cls')
        print("SET NEW DIRECTORY FOR THE XRAY FILES")
        print(Config.LINE_SEP)
        dirxrayhelper.set_file_directory()

    @staticmethod
    def do_5():
        """Info"""
        os.system('cls')
        print("INFO")
        print(Config.LINE_SEP)
        dirxrayhelper.info()

    @staticmethod
    def generate_menu():
        print(Config.TITLE)
        do_methods = [m for m in dir(Controller) if m.startswith('do_')]
        menu_string = "\n".join(
            [f"{method[-1]}.  {getattr(Controller, method).__doc__}"
             for method in do_methods if method.startswith("do_")])
        print(menu_string)
        print(f"{Config.EXIT_ACTION}", end="\n\n")

    @staticmethod
    def run(user_input=0):
        while(user_input != Config.EXIT_NUMBER):
            Controller.generate_menu()
            user_input = dirxrayhelper.get_user_input(Config.EXIT_NUMBER + 1)
            Controller.execute(user_input)
        print("Thank you for using Dir XRAY.")


def create_config_file():
    """Create a config file to the current working directory
    with the default settings if it doesn't already exist.
    """
    if not os.path.exists(os.path.join(os.getcwd(), Config.FILE)):
        config_dict = {}
        config_dict['save_to_xray_path'] = True
        config_dict['save_path'] = os.getcwd()
        try:
            with open(Config.FILE, 'w') as f:
                json.dump(config_dict, f, indent=4)
        except:
            print("Unable to create an initial config file.")
            input(Config.ENTER_CONTINUE)
            exit()
        else:
            print(f"Config file created to the path:\
            {os.path.join(os.getcwd(), Config.FILE)}.\n")


def main():
    create_config_file()
    Controller.run()


if __name__ == "__main__":
    main()

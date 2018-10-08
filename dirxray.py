import os
import json
import dirxrayhelper


class Config:
    FILE = "dirxray_config.json"
    LINE_SEP = "=" * 30
    EXIT_NUMBER = 6
    ENTER_CONTINUE = "Press <Enter> to continue."
    MENU = f"""
DIR XRAY
    DIRECTORY/FILE COMPARISON TOOL
    {LINE_SEP}
    Please type a number and press enter:
    1.  Create an xray
    2.  List xray files
    3.  Compare xray files
    4.  Set a new directory for xray files
    5.  Info
    {EXIT_NUMBER}.  Exit
        """


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
        os.system('cls')
        print("CREATE XRAY")
        print(Config.LINE_SEP)
        path = input("Enter a path: ")
        dirxrayhelper.create_xray(path)

    @staticmethod
    def do_2():
        os.system('cls')
        print("LIST OF XRAY FILES")
        print(Config.LINE_SEP)
        dirxrayhelper.list_xrays()

    @staticmethod
    def do_3():
        os.system('cls')
        print("COMPARE XRAY FILES")
        print(Config.LINE_SEP)
        dirxrayhelper.compare_xrays()

    @staticmethod
    def do_4():
        os.system('cls')
        print("SET NEW DIRECTORY FOR THE XRAY FILES")
        print(Config.LINE_SEP)
        dirxrayhelper.set_file_directory()

    @staticmethod
    def do_5():
        os.system('cls')
        print("INFO")
        print(Config.LINE_SEP)
        dirxrayhelper.info()

    @staticmethod
    def run(user_input=0):
        while(user_input != Config.EXIT_NUMBER):
            print(Config.MENU)
            user_input = dirxrayhelper.get_user_input(7)
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

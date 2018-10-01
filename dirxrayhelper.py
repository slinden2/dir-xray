import os
import json
import pathlib
import pickle
from datetime import datetime
from dirxray import Config


def get_file_data(path):
    dicti = {}
    dicti["path"] = path
    dicti["name"] = os.path.basename(path)
    dicti["size"] = os.path.getsize(path)
    dicti["creation_time"] = os.path.getctime(path)
    dicti["last_modification"] = os.path.getmtime(path)
    dicti["last_access"] = os.path.getatime(path)
    return dicti


def create_xray(path):
    """Creates an xray file of the path and saves it to the
    save location defined by `set_file_directory` function.
    :param path: A path in string format.
    """
    cumulative_dirs = []
    cumulative_files = []
    for path2, dirs, files in os.walk(path):
        for d in dirs:
            dir1 = get_file_data(os.path.join(path2, d))
            cumulative_dirs.append(dir1)
        for f in files:
            file1 = get_file_data(os.path.join(path2, f))
            cumulative_files.append(file1)

    date = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
    filename = f"xray_{date}.xray"
    save_path = get_save_path()
    try:
        with open(os.path.join(save_path, filename), 'wb') as f:
            pickle.dump([path, cumulative_dirs, cumulative_files], f, -1)
    except:
        print("An error occured while creating the file. Please try again.")
    else:
        print("The files have been saved successfully")
    finally:
        input("Press [Enter] to continue.")


def list_xrays():
    labels = ("#", "File Name", "Xray Path")
    file_list = get_file_list()
    if file_list:
        path = ""
        fn_len = len(file_list[0])
        save_path = get_save_path()
        print(f"{len(file_list)} file(s) found.")
        print(f"{labels[0]:<4} | {labels[1]:<{fn_len}} | {labels[2]}")
        for n, f in enumerate(file_list, start=1):
            try:
                with open(os.path.join(save_path, f), 'rb') as path_file:
                    file1 = pickle.load(path_file)
            except FileNotFoundError as e:
                print(f"{e}: The file is needed to show the path in\
                      the file list was not found.")
            else:
                path, _, _ = file1
            print(f"{n:<4} | {f} | {path}")
    else:
        print("No files found.")
    return file_list


def get_file_list():
    """Fetch a list of xray file from the save location."""
    path = get_save_path()
    file_list = []
    for _, _, files in os.walk(path):
        for f in files:
            if '.xray' == os.path.splitext(f)[1]:
                file_list.append(f)
    return file_list


def compare_xrays():
    """Let's the user to select from a list which xray files
    to use for comparison and print the comparison result for inspection.
    """
    print("You can select two files for comparison from the list below:")
    file_list = list_xrays()
    if file_list:
        input_len = len(file_list) + 1
        choice1 = get_user_input(input_len)
        choice2 = get_user_input(input_len)

        fn1 = file_list[choice1-1]
        fn2 = file_list[choice2-1]

        path = get_save_path()

        try:
            with open(os.path.join(path, fn1), 'rb') as f:
                file1 = pickle.load(f)
                creation_time1 = os.path.getctime(f.name)
            with open(os.path.join(path, fn2), 'rb') as f:
                file2 = pickle.load(f)
                creation_time2 = os.path.getctime(f.name)
        except FileNotFoundError as err:
            print(f"{err}: One or more of the files not found.")
        else:
            "Files loaded successfully."

        # Make sure that dirs1 and files1 come from the more recent file
        _, dirs1, files1 = file1 if creation_time1 > creation_time2 else file2
        _, dirs2, files2 = file2 if creation_time2 < creation_time1 else file1

        new_dirs, modified_dirs, removed_dirs = compare_files(dirs1, dirs2)
        new_files, modified_files, removed_files = compare_files(
            files1, files2)

        print_changed_files(new_dirs, modified_dirs, removed_dirs, 0)
        print_changed_files(new_files, modified_files, removed_files, 1)


def print_changed_files(new_files, modified_files, removed_files, n):
    """Prints all files that have been somehow changed between
    two xrays. Prints the path of the changed file and in case
    the file has been only modified, the function prints also
    the modification time.
    :param new_files: A list of new files
    :param modified_files: A list of modified files
    :param removed_files: A list of removed files
    """
    if n == 0:
        folder_file = "Folders"
    elif n == 1:
        folder_file = "Files"
    if new_files:
        print(f"Added {folder_file}")
        print(Config.LINE_SEP)
        for n, file1 in enumerate(new_files, start=1):
            print(n, file1['path'])
    if modified_files:
        print(f"Modified {folder_file}")
        print(Config.LINE_SEP)
        for n, file1 in enumerate(modified_files, start=1):
            last_mod = datetime.fromtimestamp(file1['last_modification'])
            last_mod = datetime.strftime(last_mod, "%Y-%m-%d %H:%M:%S")
            print(n, file1['path'], last_mod)
    if removed_files:
        print(f"Removed {folder_file}")
        print(Config.LINE_SEP)
        for n, file1 in enumerate(removed_files, start=1):
            print(n, file1['path'])


def set_file_directory():
    """Set a path for a directory for the xray files.
    """
    try:
        with open(Config.FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No config file found. Try restarting the program.")
        return False
    else:
        print(f"Current path: {data['save_path']}")
        new_path = input("Enter a new path: ")
        pathlib.Path(new_path).mkdir(parents=True, exist_ok=True)
        data['save_path'] = new_path
        with open(Config.FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"The path has been set to: {new_path}")


def get_save_path():
    """Fetches the save path form the config file.
    """
    try:
        with open(Config.FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"No config file found. Defaulting to {os.getcwd()}")
        path = os.getcwd()
    else:
        path = data['save_path']
    return path


def get_user_input(n):
    """Takes input from the user allowing only specific integers.

    :param n: Number of valid inputs between 1 - n
    """
    user_input = ""
    valid_inputs = [x for x in range(1, n)]
    invalid_input = "Invalid input"
    while not user_input:
        try:
            user_input = int(input("Select a number: "))
        except:
            print(invalid_input)
        else:
            if user_input not in valid_inputs:
                user_input = ""
                print(invalid_input)
    return user_input


def compare_files(file_list1, file_list2):
    """Compares input lists and returns a tuple containg
    added, modified and removed files and directories.
        :param file_list1: File list from a more recent xray.
        :param file_list2: File list from a less recent xray.
        :returns: A tuple of containing 3 items:
            -list of added files
            -list of modified files
            -list of removed files
    """
    new_files = []
    modified_files = []
    removed_files = []
    # Search added and modified files
    for file1 in file_list1:
        found = False
        modified = False
        for file2 in file_list2:
            if file2["path"] == file1["path"]:
                found = True
                if file1['last_modification'] != file2['last_modification']:
                    modified = True
        if not found:
            new_files.append(file1)
        if modified:
            modified_files.append(file1)
    # Search removed files
    for file2 in file_list2:
        found = False
        for file1 in file_list1:
            if file1["path"] == file2["path"]:
                found = True
        if not found:
            removed_files.append(file2)
    return new_files, modified_files, removed_files


def info():
    print("""Dir XRAY utility is a small software that allows you to
make xray files of you file system. Two xray files may be compared
between each other in order to see what has changed between the creation
instants of the files.

HOW TO USE IT?
Create an xray of your the folder where all your programs
are installed. Then install/remove a program to/from the same destination.
After the (un)installation is complete, create another xray of the same
destination. Now you should have two separe xrays in your file system and
you can proceed with the comparison.

The program will print out new files, modified files and removed files.

WHERE THE XRAYS ARE SAVED?
The xray files are saved by default to the same directory from where you
run the .py file. If you want to change the location, you can set it by
selecting <4> from the main menu.

LIST XRAY FILES
You may wonder why doesn't <2> List xray files discover all of your xrays.
It always searches for the xrays files from the save directory, so if you
have changed the save directory between xrays, you will find the files only
from the most recent location.
""")

    input("Press any key to continue.")

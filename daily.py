import os
from datetime import datetime

folder_name = datetime.now().strftime("%d-%m-%Y")
test_folder = os.path.join(folder_name, "Test")
file_name = folder_name + ".txt"
file_path = os.path.join(folder_name, file_name)


def make_folder():
    os.makedirs(folder_name)


def make_test():
    os.makedirs(test_folder)


def create_file():
    with open(file_path, "w") as f:
        current_date = datetime.now().strftime("------------------------------------------------------ %d-%m-%Y ------------------------------------------------------")
        f.write(current_date + "\n\n")


try:
    [print("Done. \nGet to work"), ['' if os.path.isdir(test_folder) else make_test()], [[print("File is not empty") if os.path.getsize(file_path) > 0 else create_file()] if os.path.isfile(file_path) else create_file()] if os.path.isdir(folder_name) else make_folder(), make_test()]

except Exception as e:
    print("Cannot perform operation \nReason: " + str(e))

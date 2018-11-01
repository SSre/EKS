import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_file():
    file_name = "/matilda_cost.conf"
    file_path = dir_path + file_name
    return file_path

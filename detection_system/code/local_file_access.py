"""This module handles access to local files.
    Author: Thorsten Steuer
    Company: None
    Licence: Apache 2.0
"""
#from typing import AnyStr
from beartype import beartype

class LocalFileAccess:
    """This class defines how local files can be accessed.
    """
    @beartype
    def __init__(self, local_local_file_path: str, local_file_name: str):
        """Initializes the class with a open file object.

        Args:
            local_local_file_path (str): local path to your file
            local_file_name (str): name of the file to be opened
        """
        self.local_file = open(local_local_file_path + "/" + local_file_name, "r", encoding="utf-8")

    def close(self):
        """Closes the file when called
        """
        self.local_file.close()
    @beartype
    def print_n_characters(self, n_times: int):
        """Prints n charachters of the file.

        Args:
            n_times (int): number of characters to be printed
        """
        print(self.local_file.read(n_times))

    @beartype
    def print_n_lines(self, n_times: int):
        """Prints n lines of the file.

        Args:
            n_times (int): number of lines to print
        """
        counter = 0
        for lines in self.local_file:
            if counter <= n_times:
                print("Line " + str(counter) + ": " + lines, end = "")
                counter += 1
            else:
                break


if __name__ == "__main__":
    LOCAL_PATH = "C:/Users/Thorsten/Documents/Masterarbeit/Security/ids_slow_dos/detection_system/code"
    FILE_NAME = "mosquitto.log"
    local_file = LocalFileAccess(LOCAL_PATH, FILE_NAME )
    local_file.print_n_lines(20)
    local_file.close()

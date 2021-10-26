"""This module handles access to local files.
    Author: Thorsten Steuer
    Licence: Apache 2.0
"""

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
        self.list_of_lines = self.local_file.readlines() 

    def close(self):
        """Closes the file when called
        """
        self.local_file.close()

    @beartype
    def print_n_lines(self, n_times: int):
        """Prints n lines of the file.

        Args:
            n_times (int): number of lines to print
        """
        counter = 0
        for lines in self.list_of_lines:
            if counter <= n_times:
                print("Line " + str(counter) + ": " + lines, end = "")
                counter += 1
            else:
                break

    @beartype
    def get_line(self, line_to_read: int) -> str:
        """Retruns a specific line based on the provided parameter.

        Args:
            line_to_read (int): speficies the line to be returned

        Returns:
            str: returns the requested line
        """
        return self.list_of_lines[line_to_read]

    @beartype
    def get_number_of_rows_of_file(self) -> int:
        """Retruns the amount of lines in the log file.

        Returns:
            int: number of lines
        """
        return len(self.list_of_lines)


if __name__ == "__main__":
    LOCAL_PATH = "C:/Users/Thorsten/Documents/Masterarbeit/Security/ids_slow_dos/detection_system/code"
    FILE_NAME = "mosquitto.log"
    local_file = LocalFileAccess(LOCAL_PATH, FILE_NAME)
    local_file.print_n_lines(20)
    print(local_file.get_number_of_rows_of_file())
    local_file.close()

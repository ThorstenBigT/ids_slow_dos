"""This module handles access to local files.
    Author: Thorsten Steuer
    Licence: Apache 2.0
"""

import os
import time

from beartype import beartype

class LocalFileAccess:
    """This class defines how local files can be accessed.
    """
    @beartype
    def __init__(self, local_local_file_path: str, local_file_name: str):
        """Initializes the class with a open file object. Create a list for each line and
        reset the fiel to read from the beginning.
        Args:
            local_local_file_path (str): local path to your file
            local_file_name (str): name of the file to be opened
        """
        self.local_file_path = local_local_file_path + "/" + local_file_name
        self.local_file = open(self.local_file_path, "r", encoding="utf-8")
        self.list_of_lines = self.local_file.readlines()
        self.local_file.seek(0)

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
        line_counter = 0
        for lines in self.list_of_lines:
            if line_counter <= n_times:
                print("Line " + str(line_counter) + ": " + lines, end = "")
                line_counter += 1
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

    def tail_file(self, ):
        """Follows a file like the unix comand tail. Also works if logrotate is enabled.

        Yields:
            [generator object]: returns a generator function to iterate over log lines.
        """
        seek_end = True
        while True:
            with self.local_file as file:
                if seek_end:
                    file.seek(0, 2)
                while True:
                    line = file.readline()
                    if not line:
                        try:
                            if file.tell() > os.path.getsize(self.local_file_path):
                                file.close()
                                seek_end = False
                                break
                        except FileNotFoundError:
                            pass
                        # Maybe it will be faster without sleep
                        #time.sleep(1)
                    yield line


if __name__ == "__main__":
    LOCAL_PATH = "C:/Users/Thorsten/Documents/Masterarbeit/Security/ids_slow_dos/detection_system/code"
    FILE_NAME = "mosquitto.log"
    local_file = LocalFileAccess(LOCAL_PATH, FILE_NAME)
    local_file.print_n_lines(20)
    print(local_file.get_number_of_rows_of_file())
    loglines =  local_file.tail_file()
    counter = 0
    for log_line in loglines:
        print(str(counter) + ": " + log_line)
        counter += 1
        if counter == 10:
            break
    local_file.close()

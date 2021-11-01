"""This module analizes the log entries produced by mosquitto and converts it to json.
    Author: Thorsten Steuer
    Licence: Apache 2.0
"""

import re

from beartype import beartype
from local_file_access import LocalFileAccess


class FormatLog:
    """This class contains a collection of regular expression functions to extract data
    from the log file and stores it as dataframe.
    """

    def __init__(self):
        self.client_data = {"ip_address": None,
                            "connection_to_port": None,
                            "current_time": None
                            }
        self.connection_data ={"status": "inactive",
                                "current_time": None,
                                "name": None
                                }
        self.broker_data = {"listener_port": None,
                            "version": None
                            }

    @beartype
    def extract_ip_address_by_row(self, log_string: str):
        """Extract with a regular exprsession the ip address form a string

        Args:
            log_string (str): one row of the log file
        """
        matches = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", log_string)
        if matches:
            print(str(matches[0]))
            if len(matches) == 1:
                self.client_data["ip_address"] = matches[0]
            else:
                print("Functions: extract_ip_address_by_row else clause not yet implemeneted")
        else:
            print("No match was found in: " + log_string)

    @beartype
    def extract_port_number_by_row(self, log_string: str, client=True):
        """Extract with a regular exprsession the port number form a string. Needed to
        dismiss the last two character which is the newline operator and the dot to
        properly work. In the mosquitto log the port number is everytime at the end of
        the line.
        e.g. 1635015162: New connection from 127.0.0.1 on port 1883.
        There might be a better solution for this.

        Args:
            log_string (str): one row of the log file
        """
        log_string = log_string[:-2]
        matches = re.findall(r"\b([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$\b", log_string)
        if matches:
            print(str(matches[0]))
            if len(matches) == 1:
                if client:
                    self.client_data["connection_to_port"] = matches[0]
                else:
                    self.broker_data["listener_port"] = matches[0]  
            else:
                print("Functions: extract_port_number_by_row else clause not yet implemeneted")
        else:
            print("No match was found in: " + log_string)

    @beartype
    def extract_time_in_seconds_by_row(self, log_string: str):
        """Extract  the times in seconds form a string by splitting it at the character ':'.
        Putting the timestamp each time also in the connection data start_time to tempoarily store
        in the object and check with the database.

        Args:
            log_string (str): one row of the log file
        """
        groups = log_string.split(":")
        if groups:
            print(str(groups[0]))
            self.client_data["current_time"] = groups[0]
            self.connection_data["current_time"] = groups[0]

        else:
            print("Could not split group missing ':' in: " + log_string)

    @beartype
    def extract_connection_name_by_row(self, log_string: str):
        """Extract with a regular exprsession the name of the connections.

        Args:
            log_string (str): one row of the log file
        """
        matches = re.findall(r"\b([a-z]{1,20}[-|_].[^ (]{1,20})\b", log_string)
        if matches:
            print(str(matches[0]))
            if len(matches) == 1:
                self.connection_data["name"] = matches[0]
            else:
                print("Functions: extract_connection_name_by_row else clause not yet implemeneted")
        else:
            print("No match was found in: " + log_string)

    @beartype
    def extract_version_by_row(self, log_string: str):
        """Extract with a regular exprsession the version of the broker.

        Args:
            log_string (str): one row of the log file
        """
        matches = re.findall(r"\b([0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2})\b", log_string)
        if matches:
            print(str(matches[0]))
            if len(matches) == 1:
                self.broker_data["version"] = matches[0]
            else:
                print("Functions: extract_connection_name_by_row else clause not yet implemeneted")
        else:
            print("No match was found in: " + log_string)


    @beartype
    def set_connection_status(self, status: str):
        """Set status of connection

        Args:
            status (str): status code of connection (inactive/active)
        """
        self.connection_data["status"] = status

if __name__ == "__main__":
    LOCAL_PATH = "C:/Users/Thorsten/Documents/Masterarbeit/Security/ids_slow_dos/detection_system/code"
    FILE_NAME = "mosquitto.log"
    local_file = LocalFileAccess(LOCAL_PATH, FILE_NAME)
    log_formatter = FormatLog()
    log_formatter.extract_ip_address_by_row(local_file.get_line(4))
    log_formatter.extract_port_number_by_row(local_file.get_line(4))
    log_formatter.extract_time_in_seconds_by_row(local_file.get_line(4))
    log_formatter.set_connection_status("active")
    log_formatter.extract_connection_name_by_row(local_file.get_line(5))
    log_formatter.extract_port_number_by_row(local_file.get_line(2), False)
    log_formatter.extract_version_by_row(local_file.get_line(0))
    print(log_formatter.client_data)
    print(log_formatter.connection_data)
    print(log_formatter.broker_data)
    local_file.close()
 
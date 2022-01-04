"""This module analizes the log entries produced by mosquitto and converts it to json.
    Author: Thorsten Steuer
    Licence: Apache 2.0
"""

import re
import logging

from beartype import beartype
from local_file_access import LocalFileAccess


class FormatLog:
    """This class contains a collection of regular expression functions to extract data
    from the log file and stores it as dataframe.
    """

    def __init__(self):
        """Interface to extract information from the log file. I need to use string as booleans
        since json expext them to be wirtten small an neo4j can handel the conversion.
        """
        self.host_data = {"ip_address": None,
                        "creation_time": None,
                        "is_blocked": "False",
                        "notification_sent": "False"
                        }
        self.connection_data ={"status": "active",
                                "last_update_time": None,
                                "name": None
                                }
        self.service_data = {"name": None,
                            "port": None,
                            "version": None,
                            "protocol":None,
                            }
        self.vulnerability_data = {"name": None,
                                    "cve_code": None,
                                    "effected_protocol": None,
                                    "effected_prot_version":None,
                                    "effected_app": None,
                                    "effected_app_version":None,
                                    "description": None
                                    }
        self.precondition_data = {"name": None,
                                    "type": None,
                                    "capability_level": None,
                                    "description": None
                                    }
        self.attack_data = {"name": None,
                            "type": None,
                            "goal": None
                            }

    @beartype
    def extract_ip_address_by_row(self, log_string: str):
        """Extract with a regular exprsession the ip address form a string

        Args:
            log_string (str): one row of the log file
        """
        matches = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", log_string)
        if matches:
            if len(matches) == 1:
                self.host_data["ip_address"] = matches[0]
            else:
                logging.error("Functions: extract_ip_address_by_row else clause not yet implemeneted")
        else:
            logging.info("extract_ip_address_by_row no match was found in: %s", log_string)

    @beartype
    def extract_port_number_by_row(self, log_string: str):
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
            if len(matches) == 1:
                self.service_data["port"] = matches[0]
            else:
                logging.error("Functions: extract_port_number_by_row else clause not yet implemeneted")
        else:
            logging.info("extract_port_number_by_row no match was found in: %s", log_string)

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
            self.host_data["creation_time"] = groups[0]
            self.connection_data["last_update_time"] = groups[0]

        else:
            logging.info("Could not split group missing ':' in: %s", log_string)

    @beartype
    def extract_connection_name_by_row(self, log_string: str):
        """Extract with a regular exprsession the name of the connections.

        Args:
            log_string (str): one row of the log file
        """
        matches = re.findall(r"(\w{1,}[-|_].[^ (]{1,})", log_string)
        if matches:
            if len(matches) == 1:
                self.connection_data["name"] = matches[0]
            else:
                logging.error("Functions: extract_connection_name_by_row else clause not yet implemeneted")
        else:
            logging.info("extract_connection_name_by_row no match was found in: %s", log_string)

    @beartype
    def extract_version_by_row(self, log_string: str):
        """Extract with a regular exprsession the version of the service.

        Args:
            log_string (str): one row of the log file
        """
        matches = re.findall(r"version \b([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})\b", log_string)
        if matches:
            if len(matches) == 1:
                self.service_data["version"] = matches[0]
            else:
                logging.error("Functions: extract_connection_name_by_row else clause not yet implemeneted")
        else:
            logging.info("extract_version_by_row no match was found in: %s", log_string)

    @beartype
    def set_service_port(self, port: str):
        """Set port of service

        Args:
            port (str): port of the service
        """
        self.service_data["port"] = port

    @beartype
    def set_service_protocol(self, protocol: str):
        """Set communication protocol of service

        Args:
            protocpl (str): protocol of the service
        """
        self.service_data["protocol"] = protocol

    @beartype
    def set_service_version(self, version: str):
        """Set version of service

        Args:
            protocol (str): protocol of the service
        """
        self.service_data["version"] = version

    @beartype
    def set_service_name(self, name: str):
        """Set name of service

        Args:
            name (str): name of the service
        """
        self.service_data["name"] = name

    def reset_service_data(self):
        """Set values of service_data json to None
        """
        self.service_data = dict.fromkeys(self.service_data, None)

    def reset_host_data(self):
        """Set values of host_data json to None. 
        ATTENTION!!! Only set creation_time to None ohter values are default values and the 
        ip address is neede late in the code.  
        """
        self.host_data["creation_time"] = None

    @beartype
    def set_host_is_blocked(self, is_blocked: str):
        """Set values of is_blocked in host json to false or ture.
        Is a string since neo4j can't convert python bool to json bool.

        Args:
            is_blocked (str): True or False
        """
        self.host_data["is_blocked"] = is_blocked

    @beartype
    def set_host_notification_sent(self, sent: str):
        """Set values of is_blocked in host json to false or ture.
        Is a string since neo4j can't convert python bool to json bool.
        Args:
            sent (str): True or False
        """
        self.host_data["notification_sent"] = sent

    @beartype
    def set_host_ip_address(self, ip_address: str):
        """Set values of ip_address in host json.

        Args:
            ip_address (str): ip_address of the host
        """
        self.host_data["ip_address"] = ip_address

    @beartype
    def set_host_creation_time(self, time: str):
        """Set values of creation_time in host json.

        Args:
            time (str): timestamp in second (UTC)
        """
        self.host_data["creation_time"] = time

    def reset_connection_data(self):
        """Set values of vulberability_data json to None
        """
        self.connection_data = dict.fromkeys(self.connection_data, None)

    @beartype
    def set_connection_status(self, status: str):
        """Set status of connection

        Args:
            status (str): status code of connection (inactive/active)
        """
        self.connection_data["status"] = status

    @beartype
    def set_connection_name(self, name: str):
        """Set name of connection

        Args:
            name (str): name of the connection
        """
        self.connection_data["name"] = name

    @beartype
    def set_connection_last_update_time(self, time: str):
        """Set last update time of the connection

        Args:
            time (str): time the connection was last updated
        """
        self.connection_data["last_update_time"] = time

    def reset_vulnerability_data(self):
        """Set values of connection_data json to None
        """
        self.vulnerability_data = dict.fromkeys(self.vulnerability_data, None)

    @beartype
    def set_vulnerability_name(self, name: str):
        """Set name of vulnerablitly.
        Args:
            name (str): name of the vulnerability
        """
        self.vulnerability_data["name"] = name

    @beartype
    def set_vulnerability_cve_code(self, cve_code: str):
        """Set name of vulnerablitly.
        Args:
            name (str): name of the vulnerability
        """
        self.vulnerability_data["cve_code"] = cve_code

    @beartype
    def set_vulnerability_effected_protocol(self, effected_protocol: str):
        """Set effected protocol name of vulnerablitly.
        Args:
            effected_protocol (str): name of the effected protocol
        """
        self.vulnerability_data["effected_protocol"] = effected_protocol

    @beartype
    def set_vulnerability_effected_app(self, effected_app: str):
        """Set effected app of vulnerablitly.
        Args:
            effected_app (str): name of the effected app
        """
        self.vulnerability_data["effected_app"] = effected_app

    @beartype
    def set_vulnerability_effected_app_version(self, effected_app_version: str):
        """Set effected app of vulnerablitly.
        Args:
            effected_app_version (str): name of the effected app version
        """
        self.vulnerability_data["effected_app_version"] = effected_app_version

    @beartype
    def set_vulnerability_effected_prot_version(self, effected_prot_version: str):
        """Set effected protocol version of vulnerablitly.
        Args:
            effected_prot_version (str): version of the effected protocol
        """
        self.vulnerability_data["effected_prot_version"] = effected_prot_version

    @beartype
    def set_vulnerability_description(self, description: str):
        """Set vulnerablitly description.
        Args:
            description (str): description of the vulnerability
        """
        self.vulnerability_data["description"] = description

    def reset_precondition_data(self):
        """Set values of precondition_data json to None
        """
        self.precondition_data = dict.fromkeys(self.precondition_data, None)

    @beartype
    def set_precondition_name(self, name: str):
        """Set precondition name needed for an attack.
        Args:
            description (str): name of the precondition
        """
        self.precondition_data["name"] = name

    @beartype
    def set_precondition_type(self, cond_type: str):
        """Set precondition type needed for an attack.
        Args:
            cond_type (str): type of the precondition (Network Access/User Credentials)
        """
        self.precondition_data["type"] = cond_type

    @beartype
    def set_precondition_description(self, description: str):
        """Set precondition description needed for an attack.
        Args:
            description (str): description of the precondition
        """
        self.precondition_data["description"] = description

    @beartype
    def set_precondition_capability_level(self, capability_level: str):
        """Set precondition capability_level needed for an attack.
        Args:
            capability_level (str): capability_level of the precondition
        """
        self.precondition_data["capability_level"] = capability_level

    def reset_attack_data(self):
        """Set values of precondition_data json to None
        """
        self.precondition_data = dict.fromkeys(self.precondition_data, None)

    @beartype
    def set_attack_name(self, name: str):
        """Set attack name.
        Args:
            name (str): name of the attack
        """
        self.attack_data["name"] = name

    @beartype
    def set_attack_type(self, attack_type: str):
        """Set attack type.
        Args:
            attack_type (str): name of the attack type (DoS)
        """
        self.attack_data["type"] = attack_type

    @beartype
    def set_attack_goal(self, goal: str):
        """Set attack goal.
        Args:
            goal (str): name of the attack goal
        """
        self.attack_data["goal"] = goal

if __name__ == "__main__":
    LOCAL_PATH = "C:/Users/Thorsten/Documents/Masterarbeit/Security/ids_slow_dos/detection_system/mosquitto_log_data"
    FILE_NAME = "mosquitto_test_1.log"
    local_file = LocalFileAccess(LOCAL_PATH, FILE_NAME)
    log_formatter = FormatLog()
    log_formatter.extract_ip_address_by_row(local_file.get_line(4))
    log_formatter.extract_port_number_by_row(local_file.get_line(4))
    log_formatter.extract_time_in_seconds_by_row(local_file.get_line(4))
    log_formatter.set_connection_status("active")
    log_formatter.extract_connection_name_by_row(local_file.get_line(5))
    log_formatter.extract_port_number_by_row(local_file.get_line(2))
    log_formatter.extract_version_by_row(local_file.get_line(0))
    print(log_formatter.host_data)
    print(log_formatter.connection_data)
    print(log_formatter.service_data)
    local_file.close()
 
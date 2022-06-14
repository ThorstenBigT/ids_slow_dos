"""Module to handel the mosquitto log to import it to neo4j
    Author: Thorsten Steuer
    Licence: Apache 2.0
"""
import json

# Was used for performance testing
# import time
# from statistics import median, mean, stdev


from local_file_access import LocalFileAccess
from format_log import FormatLog
from neo4j_database_access import Neo4jDatabaseAccess
from network_monitoring import NetworkMonitoring
from initialize_system import InitializeSystem

LOCAL_PATH = 'C:/kind_persistent_volume/pvc-0dd93242-6f2a-44bf-b4ee-b9879850159d_monitoring-system_mosquitto-log-pvc'
FILE_NAME = 'mosquitto.log'
NEO4J_URI = 'bolt://localhost:30687'
NEO4J_USER = 'neo4j'
NEO4J_PASS = '1234'

if __name__ == "__main__":
    local_file = LocalFileAccess(LOCAL_PATH, FILE_NAME)
    log_formatter = FormatLog()
    neo4j_driver = Neo4jDatabaseAccess(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    network_monitoring = NetworkMonitoring(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    initialize_system = InitializeSystem()
    initialize_system.demo_setup()
    network_monitoring.start()

    # Was used for performance testing
    #all_execution_times = []
    #i = 1

    loglines =  local_file.tail_file()
    for current_line in loglines:

        # Was used for performance testing
        #start_time = time.time() * 1000

        if current_line != "Socket error on client <unknown>, disconnecting.":
            log_formatter.extract_ip_address_by_row(current_line)
            log_formatter.extract_port_number_by_row(current_line)
            # Extracts time for host an connection
            log_formatter.extract_time_in_seconds_by_row(current_line)
            log_formatter.extract_connection_name_by_row(current_line)
            log_formatter.extract_version_by_row(current_line)

            if None not in log_formatter.host_data.values():
                if not neo4j_driver.check_if_node_exists('Host',
                                                        'ip_address',
                                                        log_formatter.host_data['ip_address']):
                    neo4j_driver.create_host(json.dumps(log_formatter.host_data))

            # Not sure anymore why this line is needed?
            if "/var/lib/mosquitto/mosquitto.db." in current_line:
                log_formatter.reset_connection_data()
                log_formatter.set_connection_status("active")

            if log_formatter.service_data["port"] is not None and log_formatter.service_data["version"] is not None :
                neo4j_driver.update_service_port("Mosquitto", log_formatter.service_data["port"])
                neo4j_driver.update_service_version("Mosquitto", log_formatter.service_data["version"])
                mosquitto_version = log_formatter.service_data["version"]
                mosquitto_port = log_formatter.service_data["port"]
                log_formatter.reset_service_data()

            if log_formatter.connection_data['name'] is not None and log_formatter.host_data['ip_address'] is not None:
  
                if not neo4j_driver.check_if_host_is_blocked(log_formatter.host_data['ip_address']):

                    if None not in log_formatter.connection_data.values():

                        if not neo4j_driver.check_if_node_exists('Connection',
                                                                'name',
                                                                log_formatter.connection_data['name']):
                            neo4j_driver.create_connection(json.dumps(log_formatter.connection_data))

                        if not neo4j_driver.check_if_constraint_exists('Connection', ['name']):
                            neo4j_driver.create_unique_property_constraint('Connection', ['name'])

                    if "New client connected" in current_line:
                        log_formatter.set_connection_status("active")
                        neo4j_driver.update_connection_status(log_formatter.connection_data['name'],
                                                            log_formatter.connection_data['status'])
                        neo4j_driver.update_connnection_time(log_formatter.connection_data['name'],
                                                            log_formatter.connection_data['last_update_time'])
                        starts_connection_data = ('{'
                                                    '"edge_name": "STARTS_CONNECTION",'
                                                    '"node1": {  "name":"Host",'
                                                                '"property_names": ["ip_address"],'
                                                                '"property_values": ["' + log_formatter.host_data['ip_address'] + '"]},'
                                                    '"node2": {  "name":"Connection",'
                                                                '"property_names": ["name"],'
                                                                '"property_values": ["' + log_formatter.connection_data['name'] + '"]}'
                                                    '}'
                                                )
                        neo4j_driver.create_edge(starts_connection_data)

                    if "New client connected" in current_line:

                        #Default values if nothing could be read from log file
                        if log_formatter.service_data['port'] is None or log_formatter.service_data['version'] is None:
                            log_formatter.set_service_version("1.6.9")
                            log_formatter.set_service_port("1883")

                        connects_to_data = ('{'
                                                    '"edge_name": "CONNECTS_TO",'
                                                    '"node1": { "name":"Connection",'
                                                            '"property_names": ["name"],'
                                                            '"property_values": ["' + log_formatter.connection_data['name'] + '"]},'
                                                    '"node2": {"name":"Service",'
                                                            '"property_names": ["name", "port", "version"],'
                                                            '"property_values": ["Mosquitto",'
                                                                                '"'+ log_formatter.service_data['port'] +'",'
                                                                                '"'+ log_formatter.service_data['version'] +'"]}'
                                                    '}'
                                                )
                        neo4j_driver.create_edge(connects_to_data)
                        log_formatter.reset_service_data()

                    if 'disconnected' in current_line:
                        log_formatter.set_connection_status("inactive")
                        neo4j_driver.update_connection_status(log_formatter.connection_data['name'],
                                                            log_formatter.connection_data['status'])
                        neo4j_driver.update_connnection_time(log_formatter.connection_data['name'],
                                                            log_formatter.connection_data['last_update_time'])

                    if 'disconnecting' in current_line:
                        log_formatter.set_connection_status("inactive")
                        neo4j_driver.update_connection_status(log_formatter.connection_data['name'],
                                                            log_formatter.connection_data['status'])
                        neo4j_driver.update_connnection_time(log_formatter.connection_data['name'],
                                                            log_formatter.connection_data['last_update_time'])

            log_formatter.reset_host_data()
            log_formatter.reset_connection_data()
            # Keep this here so the default value of the connection is set again
            log_formatter.set_connection_status("active")

            # Was used for performance testing
            #end_time = time.time() * 1000
            #execution_time = end_time - start_time
            #all_execution_times.append(execution_time)
            #if i == 100:
            #    all_execution_times = list(filter(lambda num: num != 0.0, all_execution_times))
            #    print(all_execution_times)
            #    print(median(all_execution_times))
            #    print(mean(all_execution_times))
            #    print(stdev(all_execution_times))
            #i = i+1


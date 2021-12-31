"""Module to handel the mosquitto log to import it to neo4j
    Author: Thorsten Steuer
    Licence: Apache 2.0
"""
from email import message
from local_file_access import LocalFileAccess
from format_log import FormatLog
from neo4j_database_access import Neo4jDatabaseAccess
from alarm_notification import AlarmNotification

LOCAL_PATH = "C:\kind_persistent_volume\pvc-de7a29b4-8af1-4480-911a-1cd1ae980e1c_monitoring-system_mosquitto-log-pvc"
FILE_NAME = "mosquitto.log"
NEO4J_URI = 'bolt://localhost:30687'
NEO4J_USER = 'neo4j'
NEO4J_PASS = 'gh1KLaqw'



if __name__ == "__main__":
    local_file = LocalFileAccess(LOCAL_PATH, FILE_NAME)
    log_formatter = FormatLog()
    neo4j_driver = Neo4jDatabaseAccess(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    email_notification = AlarmNotification()

    loglines =  local_file.tail_file()
    for current_line in loglines:
        if current_line != "Socket error on client <unknown>, disconnecting.":
 
            log_formatter.extract_ip_address_by_row(current_line)
            log_formatter.extract_port_number_by_row(current_line)
            log_formatter.extract_time_in_seconds_by_row(current_line)
            log_formatter.extract_connection_name_by_row(current_line)
            log_formatter.extract_version_by_row(current_line)
            
            if None not in log_formatter.client_data.values():
                if not neo4j_driver.check_if_node_exists('Client',
                                                        'ip_address',
                                                        log_formatter.client_data['ip_address']):
                    neo4j_driver.create_client(str(log_formatter.client_data))

                if not neo4j_driver.check_if_constraint_exists('Client', ['ip_address']):
                    neo4j_driver.create_unique_property_constraint('Client', ['ip_address'])
                    
            # Not sure anymore why this line is needed?
            if "/var/lib/mosquitto/mosquitto.db." in current_line:
                log_formatter.reset_connection_data()
                log_formatter.set_connection_status("active")

            if None not in log_formatter.broker_data.values():
                if not neo4j_driver.check_if_node_exists('Broker',
                                                        'ip_address',
                                                        log_formatter.broker_data['ip_address']):
                    neo4j_driver.create_broker(str(log_formatter.broker_data))

                if not neo4j_driver.check_if_constraint_exists('Broker', ['ip_address', 'version', 'listener_port']):
                    neo4j_driver.create_unique_property_constraint('Broker', ['ip_address', 'version', 'listener_port'])

            if log_formatter.connection_data['name'] is not None:
         
                if not neo4j_driver.check_if_client_is_blocked(log_formatter.client_data['ip_address']):

                    if None not in log_formatter.connection_data.values():

                        if not neo4j_driver.check_if_node_exists('Connection',
                                                                'name',
                                                                log_formatter.connection_data['name']):
                            neo4j_driver.create_connection(str(log_formatter.connection_data))

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
                                                    '"node1": {  "name":"Client",'
                                                                '"property_names": ["ip_address"],'
                                                                '"property_values": ["' + log_formatter.client_data['ip_address'] + '"]},'
                                                    '"node2": {  "name":"Connection",'
                                                                '"property_names": ["name"],'
                                                                '"property_values": ["' + log_formatter.connection_data['name'] + '"]}'
                                                    '}'
                                                )
                        neo4j_driver.create_edge(starts_connection_data)

                    if "New client connected" in current_line:
                        connects_to_data = ('{'
                                                    '"edge_name": "CONNECTS_TO",'
                                                    '"node1": {  "name":"Connection",'
                                                            '"property_names": ["name"],'
                                                            '"property_values": ["' + log_formatter.connection_data['name'] + '"]},'
                                                    '"node2": {  "name":"Broker",'
                                                            '"property_names": ["ip_address", "listener_port", "version"],'
                                                            '"property_values": ["'+ log_formatter.broker_data['ip_address'] +'",'
                                                                                '"'+ log_formatter.broker_data['listener_port'] +'",'
                                                                                '"'+ log_formatter.broker_data['version'] +'"]}'
                                                    '}'
                                                )
                        neo4j_driver.create_edge(connects_to_data)

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

            log_formatter.reset_client_data()
            log_formatter.reset_connection_data()
            # Keep this here so the default value of the connection is set again
            log_formatter.set_connection_status("active")

            query = (
                    'MATCH (cl:Client)-[r:STARTS_CONNECTION]->(c:Connection) '
                    'WHERE c.status = "active" AND cl.notification_sent = "False" AND cl.is_blocked = "False"'
                    'RETURN cl,count(r) as count'
                    )
            result = neo4j_driver.execute_and_return_query_result(query)
            if result is not None:
                message = ""
                for row in result:
                    if row['count'] > 50:
                        # Create Notification
                        message = message + 'Client ' + row['cl']['ip_address'] + ' has ' +  str(row['count']) + ' active connections'
                        message = message + '\n'
                        # Block Client
                        neo4j_driver.update_and_return_client_block(row['cl']['ip_address'], "True")


                if message != "":
                    email_notification.connect_to_smtp_server()
                    email_notification.send_email(message)
                    email_notification.stop_smtp()
                    neo4j_driver.update_and_return_client_notification_sent(row['cl']['ip_address'], "True")

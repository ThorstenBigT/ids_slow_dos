"""This module send a email notification if an attack is detected.

    Author: Thorsten Steuer
    Licence: Apache 2.0
"""
import json
import time

from beartype import beartype
from kubernetes import client, config

from neo4j_database_access import Neo4jDatabaseAccess
from format_log import FormatLog

NEO4J_URI = 'bolt://localhost:30687'
NEO4J_USER = 'neo4j'
NEO4J_PASS = 'gh1KLaqw'

class InitializeSystem:
    """ A class to set up the inital database set up with host, vulnearbilities etc.
    """

    def __init__(self):
        """Call initilization with database connection
        """
        self.log_formatter = FormatLog()
        self.neo4j_driver = Neo4jDatabaseAccess(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

    def demo_setup(self):
        """Set up the database for a demo use case. ATTENTION DELETE ALL ENTRIES!!
        """
        query = ('MATCH (n) DETACH DELETE n')
        self.neo4j_driver.execute_and_return_query_result(query)

        self.create_topology_set_up()
        self.create_vulnerabilities()
        self.create_attack_and_preconditions()

    def create_topology_set_up(self):
        """Creates the host and service topology of the demo use case.
        """
        # Create host machine for Neo4j
        ip_add_pod = self.get_ip_address_pod("neo4j-db")
        self.log_formatter.set_host_ip_address(ip_add_pod)
        self.log_formatter.set_host_creation_time(str(int(time.time())))

        self.neo4j_driver.create_host(json.dumps(self.log_formatter.host_data))

        # Create Service instance for Neo4j
        self.log_formatter.set_service_name("Neo4j")
        self.log_formatter.set_service_protocol("Bolt")
        self.log_formatter.set_service_version("4.3.6-enterprise")
        self.log_formatter.set_service_port("7687")

        self.neo4j_driver.create_service(json.dumps(self.log_formatter.service_data))

        self.log_formatter.reset_service_data()

        #Create a at_host relation for the neo4j service

        at_host_relation = ('{'
                            '"edge_name": "HOSTED_AT",'
                            '"node1": {  "name": "Host",'
                                        '"property_names": ["ip_address"],'
                                        '"property_values": ["' +  ip_add_pod  + '"]},'
                            '"node2": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Neo4j"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(at_host_relation)

        # Create host machine for detection system
        ip_add_pod = self.get_ip_address_pod("detection-app")
        self.log_formatter.set_host_ip_address(ip_add_pod)
        self.log_formatter.set_host_creation_time(str(int(time.time())))

        self.neo4j_driver.create_host(json.dumps(self.log_formatter.host_data))

        # Create Service instance for detection system
        self.log_formatter.set_service_name("Intrusion Detection System")
        self.log_formatter.set_service_protocol("-")
        self.log_formatter.set_service_version("0.0.1")
        self.log_formatter.set_service_port("-")

        self.neo4j_driver.create_service(json.dumps(self.log_formatter.service_data))
        self.log_formatter.reset_service_data()

        #Create a at_host relation for the detection service
        at_host_relation = ('{'
                            '"edge_name": "HOSTED_AT",'
                            '"node1": {  "name": "Host",'
                                        '"property_names": ["ip_address"],'
                                        '"property_values": ["' +  ip_add_pod  + '"]},'
                            '"node2": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Intrusion Detection System"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(at_host_relation)

        # Create a connection to neo4j database
        self.log_formatter.set_connection_name("detection-app-0a61e6f1")
        self.log_formatter.set_connection_last_update_time(str(int(time.time())))
        self.neo4j_driver.create_connection(json.dumps(self.log_formatter.connection_data))

        starts_connection_data = ('{'
                                    '"edge_name": "STARTS_CONNECTION",'
                                    '"node1": {  "name": "Host",'
                                                '"property_names": ["ip_address"],'
                                                '"property_values": ["' +  ip_add_pod  + '"]},'
                                    '"node2": {  "name":"Connection",'
                                                '"property_names": ["name"],'
                                                '"property_values": ["' +  self.log_formatter.connection_data["name"]  + '"]}'
                                    '}'
                                )

        self.neo4j_driver.create_edge(starts_connection_data)

        connects_to_data = ('{'
                            '"edge_name": "CONNECTS_TO",'
                            '"node1": {"name":"Connection",'
                                    '"property_names": ["name"],'
                                    '"property_values": ["' +  self.log_formatter.connection_data["name"]  + '"]},'
                            '"node2": {  "name":"Service",'
                                    '"property_names": ["name", "port", "version"],'
                                    '"property_values": ["Neo4j",'
                                                        '"7687",'
                                                        '"4.3.6-enterprise"]}'
                            '}'
                            )
        self.neo4j_driver.create_edge(connects_to_data)
        self.log_formatter.reset_connection_data()

        # Create host machine for mosquitto
        ip_add_pod = self.get_ip_address_pod("mosquitto-broker")
        self.log_formatter.set_host_ip_address(ip_add_pod)
        self.log_formatter.set_host_creation_time(str(int(time.time())))

        self.neo4j_driver.create_host(json.dumps(self.log_formatter.host_data))

        # Create Service instance for Mosquitto
        self.log_formatter.set_service_name("Mosquitto")
        self.log_formatter.set_service_protocol("MQTT")
        self.log_formatter.set_service_version("1.6.9")
        self.log_formatter.set_service_port("1883")

        self.neo4j_driver.create_service(json.dumps(self.log_formatter.service_data))
        self.log_formatter.reset_service_data()


        #Create a at_host relation for the mosquitto service

        at_host_relation = ('{'
                            '"edge_name": "HOSTED_AT",'
                            '"node1": {  "name": "Host",'
                                        '"property_names": ["ip_address"],'
                                        '"property_values": ["' +  ip_add_pod  + '"]},'
                            '"node2": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Mosquitto"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(at_host_relation)


        # Create host machine for one mqttsa
        ip_add_pod = self.get_ip_address_pod("mqttsa1")
        self.log_formatter.set_host_ip_address(ip_add_pod)
        self.log_formatter.set_host_creation_time(str(int(time.time())))

        self.neo4j_driver.create_host(json.dumps(self.log_formatter.host_data))

        # Create Fake Service Apache Web Service
        self.log_formatter.set_service_name("Apache Web Server")
        self.log_formatter.set_service_protocol("HTTP")
        self.log_formatter.set_service_version("2.4.52")
        self.log_formatter.set_service_port("80")

        self.neo4j_driver.create_service(json.dumps(self.log_formatter.service_data))
        self.log_formatter.reset_service_data()

        #Create a at_host relation for the apache web server service
        at_host_relation = ('{'
                            '"edge_name": "HOSTED_AT",'
                            '"node1": {  "name": "Host",'
                                        '"property_names": ["ip_address"],'
                                        '"property_values": ["' +  ip_add_pod  + '"]},'
                            '"node2": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Apache Web Server"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(at_host_relation)

    def create_vulnerabilities(self):
        """Create the vulnerabilites for the demo use case.
        """
        # Create vulnerability
        self.log_formatter.set_vulnerability_name("SlowITE")
        self.log_formatter.set_vulnerability_cve_code("CVE-2020-13849")
        self.log_formatter.set_vulnerability_effected_protocol("MQTT")
        self.log_formatter.set_vulnerability_effected_prot_version("3.1.1")
        self.log_formatter.set_vulnerability_effected_app("Mosquitto")
        self.log_formatter.set_vulnerability_effected_app_version("2.0.11 downwards")
        self.log_formatter.set_vulnerability_description("The MQTT protocol 3.1.1 requires a server to set a timeout value of 1.5 times the Keep-Alive value specified by a client, which allows remote attackers to cause a denial of service (loss of the ability to establish new connections), as demonstrated by SlowITe.")

        self.neo4j_driver.create_vulnerability(json.dumps(self.log_formatter.vulnerability_data))
        self.log_formatter.reset_vulnerability_data()

        #Create a has_vulnerability relation for the mosquitto service
        has_vulnerability_relation = ('{'
                            '"edge_name": "HAS_VULNERABILITY",'
                            '"node1": {  "name": "Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Mosquitto"]},'
                            '"node2": {  "name":"Vulnerability",'
                                        '"property_names": ["cve_code"],'
                                        '"property_values": ["CVE-2020-13849"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(has_vulnerability_relation)

        # Create vulnerability
        self.log_formatter.set_vulnerability_name("Log4j")
        self.log_formatter.set_vulnerability_cve_code("CVE-2021-44228")
        self.log_formatter.set_vulnerability_effected_protocol("-")
        self.log_formatter.set_vulnerability_effected_prot_version("-")
        self.log_formatter.set_vulnerability_effected_app("Apache Log4j")
        self.log_formatter.set_vulnerability_effected_app_version("2.15.0")
        self.log_formatter.set_vulnerability_description("An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers when message lookup substitution is enabled.")

        self.neo4j_driver.create_vulnerability(json.dumps(self.log_formatter.vulnerability_data))
        self.log_formatter.reset_vulnerability_data()

        #Create a has_vulnerability relation for the mosquitto service
        has_vulnerability_relation = ('{'
                            '"edge_name": "HAS_VULNERABILITY",'
                            '"node1": {  "name": "Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Apache Web Server"]},'
                            '"node2": {  "name":"Vulnerability",'
                                        '"property_names": ["cve_code"],'
                                        '"property_values": ["CVE-2021-44228"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(has_vulnerability_relation)


    def create_attack_and_preconditions(self):
        """Create the attacks and precondition for the demo use case
        """
        # Create attack
        self.log_formatter.set_attack_name("DoS")
        self.log_formatter.set_attack_type("SlowDoS")
        self.log_formatter.set_attack_goal("Loss of the ability to establish new connections")

        self.neo4j_driver.create_attack(json.dumps(self.log_formatter.attack_data))
        self.log_formatter.reset_attack_data()

        # Create attack
        self.log_formatter.set_attack_name("ACE")
        self.log_formatter.set_attack_type("Remote code execution")
        self.log_formatter.set_attack_goal("Arbitrary code execution (ACE) is the ability of an attacker to run any commands or code of their choice on a target machine or in a target process")

        self.neo4j_driver.create_attack(json.dumps(self.log_formatter.attack_data))
        self.log_formatter.reset_attack_data()

        # Create precondition Network Access
        self.log_formatter.set_precondition_name("Network Access")
        self.log_formatter.set_precondition_type("Reachability")
        self.log_formatter.set_precondition_capability_level("Moderate")
        self.log_formatter.set_precondition_description("To perfrom the an attack the adversary needs to have acces to the network")

        self.neo4j_driver.create_precondition(json.dumps(self.log_formatter.precondition_data))
        self.log_formatter.reset_precondition_data()

        #Create a satisfied by relation for the log4j vulnerability
        satisfied_by_relation = ('{'
                            '"edge_name": "SATISFIED_BY",'
                            '"node1": {  "name": "Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Network Access"]},'
                            '"node2": {  "name":"Vulnerability",'
                                        '"property_names": ["cve_code"],'
                                        '"property_values": ["CVE-2021-44228"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(satisfied_by_relation)

        #Create a requires relation Network Access to ACE
        requires_relation = ('{'
                            '"edge_name": "REQUIRES",'
                            '"node1": {  "name": "Attack",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["ACE"]},'
                            '"node2": {  "name":"Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Network Access"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(requires_relation)

        #Create a requires relation Network Access to DoS
        requires_relation = ('{'
                            '"edge_name": "REQUIRES",'
                            '"node1": {  "name": "Attack",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["DoS"]},'
                            '"node2": {  "name":"Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Network Access"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(requires_relation)

        #Create precondition MQTT
        self.log_formatter.set_precondition_name("MQTT 3.1.1")
        self.log_formatter.set_precondition_type("Service/Protocol Status")
        self.log_formatter.set_precondition_capability_level("Low")
        self.log_formatter.set_precondition_description("To perfrom the an attack the adversary needs to find a MQTT Broker support protocol version 3.1.1")

        self.neo4j_driver.create_precondition(json.dumps(self.log_formatter.precondition_data))
        self.log_formatter.reset_precondition_data()

        #Create a satisfied by relation for the log4j vulnerability
        satisfied_by_relation = ('{'
                            '"edge_name": "SATISFIED_BY",'
                            '"node1": {  "name": "Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["MQTT 3.1.1"]},'
                            '"node2": {  "name":"Vulnerability",'
                                        '"property_names": ["cve_code"],'
                                        '"property_values": ["CVE-2020-13849"]}'
                            '}'
                        )
        self.neo4j_driver.create_edge(satisfied_by_relation)

        #Create a requires relation Network Access to DoS
        requires_relation = ('{'
                            '"edge_name": "REQUIRES",'
                            '"node1": {  "name": "Attack",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["DoS"]},'
                            '"node2": {  "name":"Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["MQTT 3.1.1"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(requires_relation)


    @staticmethod
    @beartype
    def get_ip_address_pod(app_selector: str):
        """Gets ip address of the pod in the k8s cluster

        Args:
            app_selector (str): the app name of the pod the ip address need to be retrieved

        Returns:
            ip_address (str): ip address of the pod
        """
        # it works only if this script is run by K8s as a POD
        #config.load_incluster_config()
        config.load_kube_config()

        v_1 = client.CoreV1Api()
        ret = v_1.list_pod_for_all_namespaces(label_selector='app='+ app_selector)
        for i in ret.items:
            ip_address=i.status.pod_ip

        return ip_address

if __name__ == '__main__':
    system = InitializeSystem()
    system.demo_setup_initialization()

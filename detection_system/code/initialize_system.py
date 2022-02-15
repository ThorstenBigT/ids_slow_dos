"""This module send a email notification if an attack is detected.

    Author: Thorsten Steuer
    Licence: Apache 2.0
"""
import json
import time
import random
import uuid


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

    def perfromance_test_setup(self):
        """Set up the database for a demo use case. ATTENTION DELETE ALL ENTRIES!!
        """
        query = ('MATCH (n) DETACH DELETE n')
        self.neo4j_driver.execute_and_return_query_result(query)

        self.create_random_host(100)
        self.create_random_service(100)
        self.connect_each_service_with_a_host()
        self.connects_n_hosts_with_random_service(45,1)
        self.connects_n_hosts_with_random_service(1,55)

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
                            '"node1": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Neo4j"]},'
                            '"node2": {  "name": "Host",'
                                        '"property_names": ["ip_address"],'
                                        '"property_values": ["' +  ip_add_pod  + '"]}'
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
                            '"node1": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Intrusion Detection System"]},'
                            '"node2": {  "name": "Host",'
                                        '"property_names": ["ip_address"],'
                                        '"property_values": ["' +  ip_add_pod  + '"]}'
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
                            '"node1": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Mosquitto"]},'
                            '"node2": {  "name": "Host",'
                                        '"property_names": ["ip_address"],'
                                        '"property_values": ["' +  ip_add_pod  + '"]}'
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
                            '"node1": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Apache Web Server"]},'
                            '"node2": {  "name": "Host",'
                                        '"property_names": ["ip_address"],'
                                        '"property_values": ["' +  ip_add_pod  + '"]}'
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

        #Create a jeopardizes relation for the mosquitto service
        jeopardizes_relation = ('{'
                            '"edge_name": "JEOPARDIZES",'
                            '"node1": {  "name":"Vulnerability",'
                                        '"property_names": ["cve_code"],'
                                        '"property_values": ["CVE-2020-13849"]},'
                            '"node2": {  "name": "Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Mosquitto"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(jeopardizes_relation)

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

        #Create a jeopardizes relation for the mosquitto service
        jeopardizes_relation = ('{'
                            '"edge_name": "JEOPARDIZES",'
                            '"node1": {  "name":"Vulnerability",'
                                        '"property_names": ["cve_code"],'
                                        '"property_values": ["CVE-2021-44228"]},'
                            '"node2": {  "name": "Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Apache Web Server"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(jeopardizes_relation)


    def create_attack_and_preconditions(self):
        """Create the attacks and precondition for the demo use case
        """
        # Create attack
        self.log_formatter.set_attack_name("DoS-0a61e6f1")
        self.log_formatter.set_attack_type("SlowDoS")
        self.log_formatter.set_attack_goal("Loss of the ability to establish new connections")

        self.neo4j_driver.create_attack(json.dumps(self.log_formatter.attack_data))
        self.log_formatter.reset_attack_data()

        # Create attack
        self.log_formatter.set_attack_name("ACE-8b79e45f")
        self.log_formatter.set_attack_type("Remote code execution")
        self.log_formatter.set_attack_goal("Arbitrary code execution (ACE) is the ability of an attacker to run any commands or code of their choice on a target machine or in a target process")

        self.neo4j_driver.create_attack(json.dumps(self.log_formatter.attack_data))
        self.log_formatter.reset_attack_data()

        # Create precondition Network Access
        self.log_formatter.set_precondition_name("Network Access-f78b36b5")
        self.log_formatter.set_precondition_type("Reachability")
        self.log_formatter.set_precondition_capability_level("Moderate")
        self.log_formatter.set_precondition_description("Adversary which gain access to the network are capable to perfrom a variety of malicous actions. If this precondition is satiesfied imediate mitigation actions need to be taken")

        self.neo4j_driver.create_precondition(json.dumps(self.log_formatter.precondition_data))
        self.log_formatter.reset_precondition_data()

        #Create a satisfied by relation for the log4j vulnerability
        satisfied_by_relation = ('{'
                            '"edge_name": "SATISFIED_BY",'
                            '"node1": {  "name": "Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Network Access-f78b36b5"]},'
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
                                        '"property_values": ["ACE-8b79e45f"]},'
                            '"node2": {  "name":"Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Network Access-f78b36b5"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(requires_relation)

        #Create a requires relation Network Access to DoS
        requires_relation = ('{'
                            '"edge_name": "REQUIRES",'
                            '"node1": {  "name": "Attack",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["DoS-0a61e6f1"]},'
                            '"node2": {  "name":"Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["Network Access-f78b36b5"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(requires_relation)

        #Create precondition MQTT
        self.log_formatter.set_precondition_name("MQTT 3.1.1-a8h456u7")
        self.log_formatter.set_precondition_type("Service/Protocol Status")
        self.log_formatter.set_precondition_capability_level("Low")
        self.log_formatter.set_precondition_description("Advesaries nee first to gain access to the network befor attacking a MQTT Broker. Additionally, only specific version of the Broker implementaion may be affected. If this precondition is met mitigation actions should be taken palce wihtin weeks.")

        self.neo4j_driver.create_precondition(json.dumps(self.log_formatter.precondition_data))
        self.log_formatter.reset_precondition_data()

        #Create a satisfied by relation for the log4j vulnerability
        satisfied_by_relation = ('{'
                            '"edge_name": "SATISFIED_BY",'
                            '"node1": {  "name": "Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["MQTT 3.1.1-a8h456u7"]},'
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
                                        '"property_values": ["DoS-0a61e6f1"]},'
                            '"node2": {  "name":"Precondition",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["MQTT 3.1.1-a8h456u7"]}'
                            '}'
                        )

        self.neo4j_driver.create_edge(requires_relation)

    @beartype
    def create_random_host(self, n: int):
        """ creates n radom hosts.

        Args:
            n (int): number of host that should be created
        """
        i = 0
        for i in range(0, n):

            ip_add_pod = "196." + str(random.randint(0,10)) + "." + str(random.randint(0,244)) + "." + str(random.randint(0,244))
            self.log_formatter.set_host_ip_address(ip_add_pod)
            self.log_formatter.set_host_creation_time(str(int(time.time())))

            if not self.neo4j_driver.check_if_node_exists('Host',
                                                        'ip_address',
                                                        self.log_formatter.host_data['ip_address']):
                self.neo4j_driver.create_host(json.dumps(self.log_formatter.host_data))
                i = i + 1

            self.log_formatter.reset_host_data()

    @beartype
    def create_random_service(self, n: int):
        """Creates n random services.

        Args:
            n (int): number of services to be created
        """
        i = 0
        for i in range(0, n):
            service_list = ["Mosquitto", "Neo4j", "SSH", "Firewall", "Docker", "Kubernetes", "Apache Web Server"]
            service_name = random.choice(service_list)+ "-" + str(uuid.uuid4())
            self.log_formatter.set_service_name(service_name)
            self.log_formatter.set_service_protocol("404-Not Available")
            service_version = str(random.randint(0,30)) + "." +  str(random.randint(0,30)) + "." +  str(random.randint(0,30))
            self.log_formatter.set_service_version(service_version)
            port = str(random.randint(1000,3000))
            self.log_formatter.set_service_port(port)
    
            if not self.neo4j_driver.check_if_node_exists('Service',
                                                    'name',
                                                    self.log_formatter.service_data['name']):
                self.neo4j_driver.create_service(json.dumps(self.log_formatter.service_data))
                i = i + 1

            self.log_formatter.reset_service_data()

    def connect_each_service_with_a_host(self):
        """Connect each host with a service bia a HOSTED_AT relation

        Args:
            n (int): [description]
        """
        query = ('MATCH (h:Host) '
                'WHERE NOT (h)-[:HOSTED_AT]-(:Service) '
                'RETURN h.ip_address')
        host_result = self.neo4j_driver.execute_and_return_query_result(query)
        if host_result is not None:
            for host_row in host_result:
                query = ('MATCH (s:Service) '
                        'WHERE NOT (s)-[:HOSTED_AT]-(:Host) '
                        'return s.name')
                service_result = self.neo4j_driver.execute_and_return_query_result(query)
                service_name = random.choice(service_result)
                at_host_relation = ('{'
                        '"edge_name": "HOSTED_AT",'
                        '"node1": {  "name":"Service",'
                                    '"property_names": ["name"],'
                                    '"property_values": ["' +  service_name['s.name'] + '"]},'
                        '"node2": {  "name": "Host",'
                                    '"property_names": ["ip_address"],'
                                    '"property_values": ["' +  host_row['h.ip_address']  + '"]}'
                        '}'
                    )

                self.neo4j_driver.create_edge(at_host_relation)

    def connects_n_hosts_with_random_service(self, n_different_hosts: int, amount_of_connections: int):
        """Connect each host with a service via a connection node

        Args:
            n_different_hosts (int): number of host which should be randomly connected
            amount_of_connections (int): number of connection which should be established for this host
        """
        i = 0
        for i in range(0, n_different_hosts):
            query = ('MATCH (h:Host) '
                    'RETURN h.ip_address')
            host_result = self.neo4j_driver.execute_and_return_query_result(query)
            host_ip_address = random.choice(host_result)

            query = ('MATCH (s:Service) '
                    'return s.name')
            service_result = self.neo4j_driver.execute_and_return_query_result(query)
            service_name = random.choice(service_result)
            i = i + 1
            j = 0
            for j in range(0, amount_of_connections):
                connection_name = service_name['s.name'] + "-" + str(uuid.uuid4())
                self.log_formatter.set_connection_name(connection_name)
                self.log_formatter.set_connection_status("active")
                self.log_formatter.set_connection_last_update_time(str(int(time.time())))
                self.neo4j_driver.create_connection(json.dumps(self.log_formatter.connection_data))
                self.log_formatter.reset_connection_data()

                starts_connection_data = ('{'
                                '"edge_name": "STARTS_CONNECTION",'
                                '"node1": {  "name": "Host",'
                                            '"property_names": ["ip_address"],'
                                            '"property_values": ["' +  host_ip_address["h.ip_address"]  + '"]},'
                                '"node2": {  "name":"Connection",'
                                            '"property_names": ["name"],'
                                            '"property_values": ["' +  connection_name  + '"]}'
                                '}'
                            )

                self.neo4j_driver.create_edge(starts_connection_data)

                connects_to_data = ('{'
                                '"edge_name": "CONNECTS_TO",'
                                '"node1": {"name":"Connection",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["' +  connection_name  + '"]},'
                                '"node2": {  "name":"Service",'
                                        '"property_names": ["name"],'
                                        '"property_values": ["' + service_name['s.name'] + '"]}'
                                '}'
                                )
                self.neo4j_driver.create_edge(connects_to_data)
                j = j + 1

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
    #system.perfromance_test_setup()
   
'''This module handles CRUD operation for the Neo4j database.
https://neo4j.com/docs/api/python-driver/current/#quick-example
'''
import logging
from typing import List
import json

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from beartype import beartype


class Neo4jDatabaseAccess:
    '''This class is initialies with a neo4j database driver to communicate
    with the neo4j database instance.
    '''
    @beartype
    def __init__(self, uri: str, user: str, password: str):
        '''Consturctor to initialize the class with a database connection.

        Args:
            uri (str): [description]
            user (str): [description]
            password (str): [description]
        '''
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        '''Closes the driver object.
        '''
        self.driver.close()

    @beartype
    def create_host(self, host_json: str):
        '''Creates a host node in the database.

        Args:
            host_json (str): data of the host in json format
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_host, host_json)
            for record in result:
                print(f'Created host node: {record["h1"]}')

    @staticmethod
    def _create_and_return_host(transax, host_json: str):
        '''Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            host_json (str): data of the host in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\''+ host_json +'\') as host_data '
            'CREATE (h1:Host { ip_address: host_data.ip_address, '
                                'creation_time: host_data.creation_time, '
                                'notification_sent: host_data.notification_sent, '
                                'is_blocked: host_data.is_blocked })'
            'RETURN h1'
        )
        result = transax.run(query)
        try:
            return [{'h1': record['h1']['ip_address']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def create_connection(self, connection_json: str):
        '''Creates a connection node in the database.

        Args:
            connection_json (str): data of the connection in json format.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_connection, connection_json)
            for record in result:
                print(f'Created connection: {record["c1"]}')

    @staticmethod
    def _create_and_return_connection(transax, connection_json: str):
        '''Executes a create statement and loads in json data for new connection.

        Args:
            transax (driver.session): seesion object to execute the query
            connection_json (str): data of the connection in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\''+ connection_json +'\') as connection_data '
            'CREATE (c1:Connection { status: connection_data.status, '
                                'port: connection_data.port, '
                                'name: connection_data.name, '
                                'last_update_time: connection_data.last_update_time}) '
            'RETURN c1'
        )
        result = transax.run(query)
        try:
            return [{'c1': record['c1']['name']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def create_service(self, service_json: str):
        '''Creates a service node in the database.

        Args:
            service_json (str): data of the service in json format.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_service, service_json)
            for record in result:
                print(f'Created service node: {record["s"]}')

    @staticmethod
    def _create_and_return_service(transax, service_json: str):
        '''Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            service_json (str): data of the service in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\''+ service_json +'\') as service_data '
            'CREATE (s:Service { name: service_data.name, '
                                'port: service_data.port,'
                                'protocol: service_data.protocol,'
                                'version: service_data.version }) '
            'RETURN s'
        )
        result = transax.run(query)
        try:
            return [{'s': record['s']['name']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def create_vulnerability(self, vulnerability_json: str):
        '''Creates a vulnerability node in the database.

        Args:
            vulnerability_json (str): data of the vulnerability in json format.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_vulnerability, vulnerability_json)
            for record in result:
                print(f'Created vulnerability node: {record["v"]}')

    @staticmethod
    def _create_and_return_vulnerability(transax, vulnerability_json: str):
        '''Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            vulnerability_json (str): data of the vulnerability in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\''+ vulnerability_json +'\') as vulnerability_data '
            'CREATE (v:Vulnerability { name: vulnerability_data.name, '
                                'cve_code: vulnerability_data.cve_code,'
                                'effected_protocol: vulnerability_data.effected_protocol,'
                                'description: vulnerability_data.description,'
                                'effected_app: vulnerability_data.effected_app,'
                                'effected_app_version: vulnerability_data.effected_app_version,'
                                'effected_version: vulnerability_data.effected_prot_version}) '
            'RETURN v'
        )
        result = transax.run(query)
        try:
            return [{'v': record['v']['name']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def create_attack(self, attack_json: str):
        '''Creates a attack node in the database.

        Args:
            attack_json (str): data of the attack in json format.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_attack, attack_json)
            for record in result:
                print(f'Created attack node: {record["a"]}')

    @staticmethod
    def _create_and_return_attack(transax, attack_json: str):
        '''Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            attack_json (str): data of the attack in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\''+ attack_json +'\') as attack_data '
            'CREATE (a:Attack { name: attack_data.name, '
                                'type: attack_data.type,'
                                'goal: attack_data.goal}) '
            'RETURN a'
        )
        result = transax.run(query)
        try:
            return [{'a': record['a']['name']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def create_precondition(self, precondition_json: str):
        '''Creates a precondition node in the database.

        Args:
            precondition_json (str): data of the precondition in json format.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_precondition, precondition_json)
            for record in result:
                print(f'Created precondition node: {record["p"]}')

    @staticmethod
    def _create_and_return_precondition(transax, precondition_json: str):
        '''Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            precondition_json (str): data of the precondition in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\''+ precondition_json +'\') as precondition_data '
            'CREATE (p:Precondition { name: precondition_data.name, '
                                'type: precondition_data.type,'
                                'capability_level: precondition_data.capability_level, '
                                'description: precondition_data.goal}) '
            'RETURN p'
        )
        result = transax.run(query)
        try:
            return [{'p': record['p']['name']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise


    @beartype
    def create_edge(self,  edge_data: str):
        '''Creates a edge between two nodes in the database.

        Args:
            connection_json (str): data of the edge in json format.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_edge, edge_data)
            for record in result:
                print(f'Created edge: {record["e1"]}')

    def _create_and_return_edge(self, transax, edge_data: str):
        '''Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            connection_json (str): data of the edge in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        edge_data = json.loads(edge_data)
        where_clause = self._format_json_array_to_where_clause(edge_data['node1'],
                                                               edge_data['node2'])
        query = (
                'MATCH'
                '   (a: ' + edge_data['node1']['name'] + '), '
                '   (b: ' + edge_data['node2']['name'] + ') '
                '' + where_clause + ' '
                'CREATE (a)-[r:' + edge_data['edge_name'] + ']->(b) '
                'RETURN type(r) '
            )
        result = transax.run(query)
        try:
            return [{'e1': record['type(r)']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise


    @beartype
    def create_unique_property_constraint(self, node_name: str, property_names: List [str]):
        '''Create a unqiue property constraits for a node property.

        Args:
            node_name (str): name of the node the constraint should be applied on.
            property_name (str): name of property the constraint should be applied on.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_unique_property_constraint, node_name, property_names)
            if result is None:
                property_names_str = ''.join(property_names)
                print(f'Created unique property for node: {node_name} property: {property_names_str}')
            else:
                for record in result:
                    print(f'Created constraint: {record}')

    def _create_unique_property_constraint(self, transax, node_name: str, property_names: List [str]):
        '''Executes a create statement to add a constraint. The return value of the
        create constraint statement is a NoneType object.

        Args:
            transax (driver.session): seesion object to execute the query.
            node_name (str): name of the node the constraint should be applied on.
            property_name (str): name of property the constraint should be applied on.

        Returns:
            Iteratable: A list of dictonaries with the data from the query. In this case
            it will only return None.
        '''

        property_names = self._format_property_name_comma_list(property_names, 'n')
        query = (
            'CREATE CONSTRAINT ON (n:' + node_name + ') '
            'ASSERT ' + property_names + ' IS NODE KEY'
        )
        result = transax.run(query)
        try:
            return result
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def check_if_node_exists(self, node_name: str, property_name: str, property_value):
        '''Check if node was already created. If not checked before the neo4j throws an
        error and terminates the program.

        Args:
            node_name (str): name of the node type to check.
            property_name (str): name of the property which has unique constarint.
            property_value ([type]): value of the property.

        Returns:
            bool: Ture if node exists False otherwise.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._check_if_node_exists, node_name, property_name, property_value)
        return result

    @staticmethod
    def _check_if_node_exists(transax, node_name: str, property_name: str, property_value):
        '''Execute the query which returns True or False depending if the node exists

        Args:
            transax (driver.session): seesion object to execute the query.
            node_name (str): name of the node type to check.
            property_name (str):  name of the property which has unique constarint.
            property_value ([type]): value of the property.

        Returns:
            bool: Ture if node exists False otherwise.
        '''
        query = (
            'OPTIONAL MATCH (n:' + node_name + '{' + property_name + ':\"' + property_value + '\"})'
            'RETURN n IS NOT NULL AS exists'
        )
        result = transax.run(query)
        try:
            for record in result:
                exists = record['exists']
                if exists:
                    return True
                else:
                    return False
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def check_if_constraint_exists(self, node_name: str, property_names: List[str]):
        '''Checks if a constarint is already present in the database. Uses string
        comparison to check if in the original query was node name and proeprty
        name present.

        Args:
            node_name (str): name of the node type to check.
            property_name (str): name of the property which has unique constarint.

        Returns:
            bool: Ture if node exists False otherwise
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._check_if_constraint_exists, node_name, property_names)
        return result

    def _check_if_constraint_exists(self, transax, node_name: str, property_names: str):
        '''Executes query to call db.straints which returns a list of all constraints
        in the database.

        Args:
            transax (driver.session): seesion object to execute the query.
            node_name (str): name of the node type to check.
            property_name (str): name of the property which has unique constarint.

        Returns:
            bool: Ture if node exists False otherwise
        '''
        query = (
           'CALL db.constraints'
        )
        result = transax.run(query)
        try:
            evaluation = False
            property_names = self._format_property_name_comma_list(property_names, node_name.lower())
            constraint = (
                'CONSTRAINT ON ( ' + node_name.lower() + ':' + node_name + ' ) '
                'ASSERT ' + property_names + ' IS NODE KEY'
            )

            for record in result:
                description = record['description']
                if constraint in description:
                    evaluation = True

            return evaluation
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def check_if_host_is_blocked(self, ip_address: str):
        """Checks if a host is blocked for new incoming connection or not.
        Args:
            ip_address (str): ip address of host to verify

        Returns:
            bool: Ture if host is currently blocked
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self. _check_if_host_is_blocked, ip_address)
        return result

    def _check_if_host_is_blocked(self, transax, ip_address: str):
        """Executes querz to check the block status of a host.

        Args:
            transax (driver.session): seesion object to execute the query.
            ip_address (str): the ip address of the host to be verified

        Returns:
            bool: Ture if host is currently blocked
        """
        query = (
                        'MATCH (h1:Host) '
                        'WHERE h1.ip_address = "' + ip_address + '"'
                        'RETURN h1'
                        )

        result = transax.run(query)

        try:
            is_blocked = False
            for record in result:
                is_blocked=record['h1']['is_blocked']

            if is_blocked == "True":
                return True
            else:
                return False
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def update_connection_status(self, connection_name: str, status: str):
        """Updates the status of a connection to active or inactive

        Args:
            connection_name (str): name of the connection to be updated
            status (str): status to be set for the connection
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._update_and_return_connection_status, connection_name, status)
        for record in result:
            print(f'Updated Connection Status: {record}')

    @staticmethod
    @beartype
    def _update_and_return_connection_status(transax, connection_name: str, status: str):
        """Executes the update query for a specific connection.

        Args:
            transax (driver.session): seesion object to execute the query
            connection_name (str): the connection to be updated
            status (str): the status to be set for the speficied conenction

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
                'MATCH (c:Connection {name: "' + connection_name + '"}) '
                'SET c.status = "' + status + '" '
                'RETURN c'
                )
        result = transax.run(query)
        try:
            return [{'c': record['c']['name']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def update_and_return_host_block(self, ip_address: str, is_blocked: str):
        """ Updates the block status of a host. Will be set to True if a hosts
            creates to many active connections.

        Args:
            ip_address (str): ip_address of the host to be blocked
            is_blocked (bool): state of the block status (True/False)
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._update_and_return_host_block, ip_address, is_blocked)
        for record in result:
            print(f'Updated block status of host: {record}')

    @staticmethod
    @beartype
    def _update_and_return_host_block(transax, ip_address: str, is_blocked: str):
        """Execute the query to update the host block status.

        Args:
            transax (driver.session): seesion object to execute the query
            ip_address (str): the hosts ip address to be updated
            is_blocked (str): the status to be set (Ture or False)

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
                'MATCH (h:Host {ip_address: "' + ip_address + '"}) '
                'SET h.is_blocked = "' + is_blocked + '" '
                'RETURN h'
                )
        result = transax.run(query)
        try:
            return [{'h': record['h']['ip_address']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def update_and_return_host_notification_sent(self, ip_address: str, sent: str):
        """ Updates the notification status of a host. Once it was blocked an email
        is sent to the admin to notify the precondition.

        Args:
            ip_address (str): ip_address of the host to be blocked
            sent (bool): state of the notification status (True/False)
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._update_and_return_host_notification_sent, ip_address, sent)
        for record in result:
            print(f'Updated notification sent of host: {record}')

    @staticmethod
    @beartype
    def _update_and_return_host_notification_sent(transax, ip_address: str, sent: str):
        """Execute the query to update the notification status of the host.

        Args:
            transax (driver.session): seesion object to execute the query
            ip_address (str): the ip address of the host to be updated
            sent (str): status to be set (Ture or False)

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
                'MATCH (h:Host {ip_address: "' + ip_address + '"}) '
                'SET h.notification_sent = "' + sent + '" '
                'RETURN h'
                )
        result = transax.run(query)
        try:
            return [{'h': record['h']['ip_address']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def update_connnection_time(self, connection_name: str, time: str):
        """Updates the connection node with the latest timestamp when it was
        last updated.

        Args:
            connection_name (str): name of the connection
            time (str): the timestamp to set
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._update_and_return_connection_time, connection_name, time)
        for record in result:
            print(f'Updated Connection Time: {record}')

    @staticmethod
    @beartype
    def _update_and_return_connection_time(transax, connection_name: str, time: str):
        """Executes the update query for a specific connection.

        Args:
            transax (driver.session): seesion object to execute the query
            connection_name (str): the connection to be updated
            time (str): the time to be set for the speficied conenction

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
                'MATCH (c:Connection {name: "' + connection_name + '"}) '
                'SET c.last_update_time = "' + time + '" '
                'RETURN c'
                )
        result = transax.run(query)
        try:
            return [{'c': record['c']['name']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def update_service_version(self, service_name: str, version: str):
        """Updates the service node with the version from the log file.

        Args:
            service_name (str): name of the service
            version (str): version of the service
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._update_and_return_service_version, service_name, version)
        for record in result:
            print(f'Updated service version: {record}')

    @staticmethod
    @beartype
    def _update_and_return_service_version(transax, service_name: str, version: str):
        """Executes the update query for a specific service.

        Args:
            transax (driver.session): seesion object to execute the query
            service_name (str): the service to be updated
            version (str): the version to be set for the speficied service

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
                'MATCH (s:Service {name: "' + service_name + '"}) '
                'SET s.version = "' + version + '" '
                'RETURN s'
                )
        result = transax.run(query)
        try:
            return [{'s': record['s']['version']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def update_service_port(self, service_name: str, port: str):
        """Updates the service node with the port from the log file.

        Args:
            service_name (str): name of the service
            port (str): port of the service
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._update_and_return_service_port, service_name, port)
        for record in result:
            print(f'Updated service port: {record}')

    @staticmethod
    @beartype
    def _update_and_return_service_port(transax, service_name: str, port: str):
        """Executes the update query for a specific service.

        Args:
            transax (driver.session): seesion object to execute the query
            service_name (str): the service to be updated
            port (str): the port to be set for the speficied service

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
                'MATCH (s:Service {name: "' + service_name + '"}) '
                'SET s.port = "' + port + '" '
                'RETURN s'
                )
        result = transax.run(query)
        try:
            return [{'s': record['s']['port']}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise

    @beartype
    def execute_and_return_query_result(self, query: str):
        """Execute a query based on the chyper string provided

        Args:
            query (str): a chyper query

        Returns:
            result (list): a list of dictonary each row of the result a dict
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._execute_and_return_query_result, query)
            return result

    @staticmethod
    @beartype
    def _execute_and_return_query_result(transax, query):
        """Exectues a query provided by the query parameter

        Args:
            transax (driver.session): seesion object to execute the query
            query (str): a chyper query

        Returns:
            [type]: [description]
        """
        result = transax.run(query)
        try:
            return result.data()
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error('%s raised an error: \n %s', query, exception)
            raise


    @staticmethod
    @beartype
    def _format_property_name_comma_list(data: List[str], short_name: str):
        """Format property name from list to chyper query snytax

        Args:
            data (List[str]): a list of property name strings
            short_name (str): the acronmy use in the chyper query

        Returns:
            [str]: a string containing the property names in the proper chyper format
        """
        if len(data) == 1:
            return '(' + short_name + '.' + data[0] + ')'
        else:
            entries = ''
            for entry in data:
                entries = entries + short_name + '.' + entry + ', '
            formated_entries = entries[:-2]
            formated_entries = '(' + formated_entries + ')'
            return formated_entries

    @staticmethod
    @beartype
    def _format_json_array_to_where_clause(node1: dict, node2: dict):
        """Format the two node description jason the a where clause to create
        a realtion between two nodes.

        Args:
            node1 (dict): description of the first node to match
            node2 (dict): description of the second node to match

        Returns:
            [str]: properly formated chyper where clause
        """
        if len(node1['property_names']) == 1 and node2['property_names'] == 1:
            where_clause=(
                'WHERE a.' + node1['property_names'][0] + '=\"' + node1['property_values'][0] + '\" '
                'and b.' + node2['property_names'][0] + '=\"' + node2['property_values'][0] + '\"'
                 )
        else:
            temp_str = ""
            for i in range(0, len(node1['property_names'])):
                temp_str = (
                    temp_str + 'a.' + node1['property_names'][i] + '=\"'
                    + node1['property_values'][i] + "\" and "
                )
            for i in range(0, len(node2['property_names'])):
                temp_str = (
                    temp_str + 'b.' + node2['property_names'][i] + '=\"'
                    + node2['property_values'][i] + "\" and "
                )
            where_clause = temp_str[:-4]
            where_clause = 'Where '+ where_clause
        return where_clause



if __name__ == '__main__':
    DUMMY_DATA_FOLDER_PATH = 'C:/Users/Thorsten/Documents/Masterarbeit/Security/ids_slow_dos/detection_system/code/dummy_data'

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_host_data.json', encoding='utf-8')
    HOST_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_connection_data.json', encoding='utf-8')
    CONNECTION_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_service_data.json', encoding='utf-8')
    SERVICE_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_starts_connection_data.json', encoding='utf-8')
    STARTS_CONNECTION_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_connects_to_data.json', encoding='utf-8')
    CONNECTS_TO_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_hosted_at_data.json', encoding='utf-8')
    HOSTED_AT_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_vulnerability_data.json', encoding='utf-8')
    VULNERABILITY_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_has_vulnerability_data.json', encoding='utf-8')
    HAS_VULNERABILITY_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_attack_data.json', encoding='utf-8')
    ATTACK_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_exploits_data.json', encoding='utf-8')
    EXPLOITS_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_precondition_data.json', encoding='utf-8')
    PRECONDITION_DATA_TEST = json.loads(f.read())
    f.close()

    f = open(DUMMY_DATA_FOLDER_PATH + '/sample_requires_data.json', encoding='utf-8')
    REQUIRES_DATA_TEST = json.loads(f.read())
    f.close()

    NEO4J_URI = 'bolt://localhost:30687'
    NEO4J_USER = 'neo4j'
    NEO4J_PASS = 'gh1KLaqw'

    neo4j_driver = Neo4jDatabaseAccess(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

    if not neo4j_driver.check_if_node_exists('Host', 'ip_address', '127.0.0.1'):
        neo4j_driver.create_host(json.dumps(HOST_DATA_TEST))
    if not neo4j_driver.check_if_constraint_exists('Host', ['ip_address']):
        neo4j_driver.create_unique_property_constraint('Host', ['ip_address'])

    if not neo4j_driver.check_if_node_exists('Connection', 'name', 'mqtt-explorer-0a61e6f1'):
        neo4j_driver.create_connection(json.dumps(CONNECTION_DATA_TEST))
    if not neo4j_driver.check_if_constraint_exists('Connection', ['name']):
        neo4j_driver.create_unique_property_constraint('Connection', ['name'])

    if not neo4j_driver.check_if_node_exists('Service', 'name', 'mosquitto'):
        neo4j_driver.create_service(json.dumps(SERVICE_DATA_TEST))
    if not neo4j_driver.check_if_constraint_exists('Service', ['name', 'version', 'port']):
        neo4j_driver.create_unique_property_constraint('Service', ['name', 'version', 'port'])

    if not neo4j_driver.check_if_node_exists('Vulnerability', 'cve_code', 'CVE-2020-13849'):
        neo4j_driver.create_vulnerability(json.dumps(VULNERABILITY_DATA_TEST))
    if not neo4j_driver.check_if_constraint_exists('Vulnerability', ['cve_code']):
        neo4j_driver.create_unique_property_constraint('Vulnerability', ['cve_code'])

    if not neo4j_driver.check_if_node_exists('Attack', 'name', 'DoS'):
        neo4j_driver.create_attack(json.dumps(ATTACK_DATA_TEST))
    if not neo4j_driver.check_if_constraint_exists('Attack', ['name', 'type']):
        neo4j_driver.create_unique_property_constraint('Attack', ['name', 'type'])

    if not neo4j_driver.check_if_node_exists('Precondition', 'name', 'Network Access'):
        neo4j_driver.create_precondition(json.dumps(PRECONDITION_DATA_TEST))
    if not neo4j_driver.check_if_constraint_exists('Precondition', ['name', 'type']):
        neo4j_driver.create_unique_property_constraint('Precondition', ['name', 'type'])

    neo4j_driver.create_edge(json.dumps(STARTS_CONNECTION_DATA_TEST))
    neo4j_driver.create_edge(json.dumps(CONNECTS_TO_DATA_TEST))
    neo4j_driver.create_edge(json.dumps(HOSTED_AT_DATA_TEST))
    neo4j_driver.create_edge(json.dumps(HAS_VULNERABILITY_DATA_TEST))
    neo4j_driver.create_edge(json.dumps(EXPLOITS_DATA_TEST))
    neo4j_driver.create_edge(json.dumps(REQUIRES_DATA_TEST))

    neo4j_driver.update_connection_status('mqtt-explorer-0a61e6f1', 'active')
    neo4j_driver.update_connnection_time('mqtt-explorer-0a61e6f1', '1635015166')

    COUNT_QUERY = (
            'MATCH (h:Host)-[r:STARTS_CONNECTION]->() '
            'RETURN h, count(r) as count'
             )
    count_result = neo4j_driver.execute_and_return_query_result(COUNT_QUERY)

    if count_result is not None:
        for records in count_result:
            print(records)

    neo4j_driver.close()

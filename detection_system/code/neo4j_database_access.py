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
    def create_client(self, client_json: str):
        '''Creates a client node in the database.

        Args:
            client_json (str): data of the client in json format
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_client, client_json)
            for record in result:
                print(f'Created client node: {record["c1"]}')

    @staticmethod
    def _create_and_return_client(transax, client_json: str):
        '''Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            client_json (str): data of the client in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\"'+ client_json +'\") as client_data '
            'CREATE (c1:Client { ip_address: client_data.ip_address, '
                                'current_time: client_data.current_time })'
            'RETURN c1'
        )
        result = transax.run(query)
        try:
            return [{'c1': record['c1']['ip_address']}
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
            client_json (str): data of the connection in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\"'+ connection_json +'\") as connection_data '
            'CREATE (c1:Connection { status: connection_data.status, '
                                'port: connection_data.port, '
                                'name: connection_data.name, '
                                'current_time: connection_data.current_time}) '
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
    def create_broker(self, broker_json: str):
        '''Creates a broker node in the database.

        Args:
            connection_json (str): data of the broker in json format.
        '''
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_broker, broker_json)
            for record in result:
                print(f'Created broker node: {record["b"]}')

    @staticmethod
    def _create_and_return_broker(transax, broker_json: str):
        '''Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            client_json (str): data of the broker in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        '''
        query = (
            'WITH apoc.convert.fromJsonMap(\"'+ broker_json +'\") as broker_data '
            'CREATE (b:Broker { listener_port: broker_data.listener_port, '
                                'ip_address: broker_data.ip_address,'
                                'version: broker_data.version }) '
            'RETURN b'
        )
        result = transax.run(query)
        try:
            return [{'b': record['b']['ip_address']}
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
            client_json (str): data of the edge in json format

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
    def update_and_return_client_block(self, connection_name: str, status: str):
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
    def _update_and_return_client_block(transax, connection_name: str, status: str):
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
    def update_connnection_time(self, connection_name: str, time: str):
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
                'SET c.current_time = "' + time + '" '
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
    CLIENT_DATA_TEST = '{"ip_address": "127.0.0.1", "current_time": "1635015162"}'
    CONNECTION_DATA_TEST = '''{"status": "active", "current_time": "1635015162",
                               "port": "1883", "name": "mqtt-explorer-0a61e6f1"}'''
    BROKER_DATA_TEST = '{"listener_port": "1883", "version": "1.6.9", "ip_address": "127.0.0.1"}'
    STARTS_CONNECTION_DATA_TEST = '''{"edge_name": "STARTS_CONNECTION",
                                        "node1": {  "name":"Client",
                                                    "property_names": ["ip_address"],
                                                    "property_values": ["127.0.0.1"]},
                                        "node2": {  "name":"Connection",
                                                    "property_names": ["name"],
                                                    "property_values": ["mqtt-explorer-0a61e6f1"]}
                                        }'''
    CONNECTS_TO_DATA_TEST = '''{"edge_name": "CONNECTS_TO",
                                    "node1": {  "name":"Connection",
                                                "property_names": ["name"],
                                                "property_values": ["mqtt-explorer-0a61e6f1"]},
                                    "node2": {  "name":"Broker",
                                                "property_names": ["ip_address", "listener_port", "version"],
                                                "property_values": ["127.0.0.1", "1883", "1.6.9"]}
                                    }'''
    NEO4J_URI = 'bolt://localhost:7687'
    NEO4J_USER = 'neo4j'
    NEO4J_PASS = 'gh1KLaqw'

    neo4j_driver = Neo4jDatabaseAccess(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

    if not neo4j_driver.check_if_node_exists('Client', 'ip_address', '127.0.0.1'):
        neo4j_driver.create_client(CLIENT_DATA_TEST)
    if not neo4j_driver.check_if_constraint_exists('Client', ['ip_address']):
        neo4j_driver.create_unique_property_constraint('Client', ['ip_address'])

    if not neo4j_driver.check_if_node_exists('Connection', 'name', 'mqtt-explorer-0a61e6f1'):
        neo4j_driver.create_connection(CONNECTION_DATA_TEST)
    if not neo4j_driver.check_if_constraint_exists('Connection', ['name']):
        neo4j_driver.create_unique_property_constraint('Connection', ['name'])

    if not neo4j_driver.check_if_node_exists('Broker', 'ip_address', '127.0.0.1'):
        neo4j_driver.create_broker(BROKER_DATA_TEST)
    if not neo4j_driver.check_if_constraint_exists('Broker', ['ip_address', 'version', 'listener_port']):
        neo4j_driver.create_unique_property_constraint('Broker', ['ip_address', 'version', 'listener_port'])

    neo4j_driver.create_edge(STARTS_CONNECTION_DATA_TEST)
    neo4j_driver.create_edge(CONNECTS_TO_DATA_TEST)
    neo4j_driver.update_connection_status('mqtt-explorer-0a61e6f1', 'active')
    neo4j_driver.update_connection_status('mqtt-explorer-0a61e6f1', '1635015166')

    count_query = (
            'MATCH (c:Client)-[r:STARTS_CONNECTION]->() '
            'RETURN c, count(r) as count'
             )
    count_result = neo4j_driver.execute_and_return_query_result(count_query)

    if count_result is not None:
        for records in count_result:
            print(records)

    neo4j_driver.close()

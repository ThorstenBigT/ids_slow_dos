"""This module handles CRUD operation for the Neo4j database.
"""
import logging
from typing import List

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from beartype import beartype


class Neo4jDatabaseAccess:
    """This class is initialies with a neo4j database driver to communicate
    with the neo4j database instance.
    """

    def __init__(self, uri: str, user: str, password: str):
        """Consturctor to initialize the class with a database connection.

        Args:
            uri (str): [description]
            user (str): [description]
            password (str): [description]
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Closes the driver object.
        """
        self.driver.close()

    @beartype
    def create_client(self, client_json: str):
        """Creates a client node in the database.

        Args:
            client_json (str): data of the client in json format
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_client, client_json)
            for record in result:
                print(f"Created client node: {record['c1']}")

    @staticmethod
    def _create_and_return_client(transax, client_json: str):
        """Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            client_json (str): data of the client in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
            "WITH apoc.convert.fromJsonMap(\""+ client_json +"\") as client_data "
            "CREATE (c1:Client { ip_address: client_data.ip_address, "
                                "current_time: client_data.current_time })"
            "RETURN c1"
        )
        result = transax.run(query)
        try:
            return [{"c1": record["c1"]["ip_address"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("%s raised an error: \n %s", query, exception)
            raise

    @beartype
    def create_connection(self, connection_json: str):
        """Creates a connection node in the database.

        Args:
            connection_json (str): data of the connection in json format.
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_connection, connection_json)
            for record in result:
                print(f"Created client node: {record['c1']}")

    @staticmethod
    def _create_and_return_connection(transax, connection_json: str):
        """Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            client_json (str): data of the connection in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
            "WITH apoc.convert.fromJsonMap(\""+ connection_json +"\") as connection_data "
            "CREATE (c1:Connection { status: connection_data.status, "
                                "port: connection_data.port, "
                                "name: connection_data.name, "
                                "current_time: connection_data.current_time}) "
            "RETURN c1"
        )
        result = transax.run(query)
        try:
            return [{"c1": record["c1"]["name"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("%s raised an error: \n %s", query, exception)
            raise

    @beartype
    def create_broker(self, broker_json: str):
        """Creates a broker node in the database.

        Args:
            connection_json (str): data of the broker in json format.
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_connection, broker_json)
            for record in result:
                print(f"Created client node: {record['b1']}")

    @staticmethod
    def _create_and_return_broker(transax, broker_json: str):
        """Executes a create statement and loads in json data.

        Args:
            transax (driver.session): seesion object to execute the query
            client_json (str): data of the broker in json format

        Returns:
            Iteratable: A list of dictonaries with the data from the query.
        """
        query = (
            "WITH apoc.convert.fromJsonMap(\""+ broker_json +"\") as broker_data "
            "CREATE (c1:Broker { listener_port: broker_data.listener_port, "
                                "ip_address: broker_data.ip_address",
                                "version: broker_data.version }) "
            "RETURN b1"
        )
        result = transax.run(query)
        try:
            return [{"b1": record["b1"]["name"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("%s raised an error: \n %s", query, exception)
            raise


    @beartype
    def create_unique_property_constraint(self, node_name: str, property_names: List [str]):
        """Create a unqiue property constraits for a node property.

        Args:
            node_name (str): name of the node the constraint should be applied on.
            property_name (str): name of property the constraint should be applied on.
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_unique_property_constraint, node_name, property_names)
            if result is None:
                property_names_str = "".join(property_names)
                print(f"Created unique property for node: {node_name} property: {property_names_str}")
            else:
                for record in result:
                    print(f"Created constraint: {record}")

    def _create_unique_property_constraint(self, transax, node_name: str, property_names: List [str]):
        """Executes a create statement to add a constraint. The return value of the
        create constraint statement is a NoneType object.

        Args:
            transax (driver.session): seesion object to execute the query.
            node_name (str): name of the node the constraint should be applied on.
            property_name (str): name of property the constraint should be applied on.

        Returns:
            Iteratable: A list of dictonaries with the data from the query. In this case
            it will only return None.
        """

        property_names = self._format_property_name_comma_list(property_names, "c.")
        query = (
            "CREATE CONSTRAINT ON (c:" + node_name + ") "
            "ASSERT " + property_names + " IS NODE KEY"
        )
        result = transax.run(query)
        try:
            return result
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("%s raised an error: \n %s", query, exception)
            raise

    @beartype
    def check_if_node_exists(self, node_name: str, property_name: str, property_value):
        """Check if node was already created. If not checked before the neo4j throws an
        error and terminates the program.

        Args:
            node_name (str): name of the node type to check.
            property_name (str): name of the property which has unique constarint.
            property_value ([type]): value of the property.

        Returns:
            bool: Ture if node exists False otherwise.
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._check_if_node_exists, node_name, property_name, property_value)
        return result

    @staticmethod
    def _check_if_node_exists(transax, node_name: str, property_name: str, property_value):
        """Execute the query which returns True or False depending if the node exists

        Args:
            transax (driver.session): seesion object to execute the query.
            node_name (str): name of the node type to check.
            property_name (str):  name of the property which has unique constarint.
            property_value ([type]): value of the property.

        Returns:
            bool: Ture if node exists False otherwise.
        """
        query = (
            "OPTIONAL MATCH (c:" + node_name + "{" + property_name + ":\"" + property_value + "\"})"
            "RETURN c IS NOT NULL AS exists"
        )
        result = transax.run(query)
        try:
            for record in result:
                exists = record["exists"]
                if exists:
                    return True
                else:
                    return False
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("%s raised an error: \n %s", query, exception)
            raise

    @beartype
    def check_if_constraint_exists(self, node_name: str, property_names: List[str]):
        """Checks if a constarint is already present in the database. Uses string
        comparison to check if in the original query was node name and proeprty
        name present.

        Args:
            node_name (str): name of the node type to check.
            property_name (str): name of the property which has unique constarint.

        Returns:
            bool: Ture if node exists False otherwise
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._check_if_constraint_exists, node_name, property_names)
        return result

    @staticmethod
    def _check_if_constraint_exists(transax, node_name: str, property_names: List [str]):
        """Executes query to call db.straints which returns a list of all constraints
        in the database.

        Args:
            transax (driver.session): seesion object to execute the query.
            node_name (str): name of the node type to check.
            property_name (str): name of the property which has unique constarint.

        Returns:
            bool: Ture if node exists False otherwise
        """
        query = (
           "CALL db.constraints"
        )
        result = transax.run(query)
        try:
            for record in result:
                description = record["description"]
                evaluation = False
                for name in property_names:
                    if node_name in description and name in description:
                        evaluation = True
                    else:
                        evaluation = False

            return evaluation
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("%s raised an error: \n %s", query, exception)
            raise

    @staticmethod
    def _format_property_name_comma_list(data: List[str], short_name: str):

        if len(data) == 1:
            return short_name + data[0]
        else:
            entries = ""
            for entry in data:
                entries = entries + short_name + entry + ","
            formated_entries = entries[:-1]
            formated_entries = "(" + formated_entries + ")"
            return formated_entries


if __name__ == "__main__":
    CLIENT_DATA_TEST = "{'ip_address': '127.0.0.1', 'current_time': '1635015162'}"
    CONNECTION_DATA_TEST = """{'status': 'active', 'current_time': '1635015162',
                               'port': '1883', 'name': 'mqtt-explorer-0a61e6f1'}"""
    BROKER_DATA_TEST = "{'listener_port': '1883', 'version': '1.6.9', 'ip_address': '127.0.0.1'}"
    NEO4J_URI = "bolt://localhost:30687"
    NEO4J_USER = "neo4j"
    NEO4J_PASS = "gh1KLaqw"
    neo4j_driver = Neo4jDatabaseAccess(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

    if not neo4j_driver.check_if_node_exists("Client", "ip_address", "127.0.0.1"):
        neo4j_driver.create_client(CLIENT_DATA_TEST)
    if not neo4j_driver.check_if_constraint_exists("Client", ["ip_address"]):
        neo4j_driver.create_unique_property_constraint("Client", ["ip_address"])

    if not neo4j_driver.check_if_node_exists("Connection", "name", "mqtt-explorer-0a61e6f1"):
        neo4j_driver.create_connection(CONNECTION_DATA_TEST)
    if not neo4j_driver.check_if_constraint_exists("Connection", ["name"]):
        neo4j_driver.create_unique_property_constraint("Connection", ["name"])

    if not neo4j_driver.check_if_node_exists("Broker", "ip_addresse", "127.0.0.1"):
        neo4j_driver.create_connection(BROKER_DATA_TEST)
    if not neo4j_driver.check_if_constraint_exists("Broker", ["ip_addresse", "version", "listener_port"]):
        neo4j_driver.create_unique_property_constraint("Broker", ["ip_addresse", "version", "listener_port"])

    """ NEO4J DOES NOT SUPPORT MULTPY PROPERTY CONSTRAINTS IN COMMUNITY VERSION CHECK ENTERPRISE ACCESS """
    neo4j_driver.close()

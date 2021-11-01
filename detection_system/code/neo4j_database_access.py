"""This module handles CRUD operation for the Neo4j database.
"""
import logging

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
                                "connection_to_port: client_data.connection_to_port, "
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
    def create_unique_property_constraint(self, node_name: str, property_name: str):
        """Create a unqiue property constraits for a node property.

        Args:
            node_name (str): name of the node the constraint should be applied on.
            property_name (str): name of property the constraint should be applied on.
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_unique_property_constraint, node_name, property_name)
            if result is None:
                print(f"Created unique property for node: {node_name} property: {property_name}")
            else:
                for record in result:
                    print(f"Created client node: {record}")

    @staticmethod
    def _create_unique_property_constraint(transax, node_name: str, property_name: str):
        """Executes a create statement to add a constraint. The return value of the
        create constraint statement is a NoneType object.

        Args:
            transax (driver.session): seesion object to execute the query
            node_name (str): name of the node the constraint should be applied on.
            property_name (str): name of property the constraint should be applied on.

        Returns:
            Iteratable: A list of dictonaries with the data from the query. In this case
            it will only return None.
        """
        query = (
            "CREATE CONSTRAINT ON (c:" + node_name + ") ASSERT c." + property_name + " IS UNIQUE"
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
        """[summary]

        Args:
            node_name (str): [description]
            property_name (str): [description]
            property_value ([type]): [description]

        Returns:
            [type]: [description]
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._check_if_node_exists, node_name, property_name, property_value)
        return result

    @staticmethod
    def _check_if_node_exists(transax, node_name: str, property_name: str, property_value):
        """[summary]

        Args:
            transax ([type]): [description]
            node_name (str): [description]
            property_name (str): [description]
            property_value ([type]): [description]

        Returns:
            [type]: [description]
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
    def check_if_constraint_exists(self, node_name: str, property_name: str):
        """[summary]

        Args:
            node_name (str): [description]
            property_name (str): [description]

        Returns:
            [type]: [description]
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._check_if_constraint_exists, node_name, property_name)
        return result

    @staticmethod
    def _check_if_constraint_exists(transax, node_name: str, property_name: str):
        """[summary]

        Args:
            transax ([type]): [description]
            node_name (str): [description]
            property_name (str): [description]

        Returns:
            [type]: [description]
        """
        query = (
           "CALL db.constraints"
        )
        result = transax.run(query)
        try:
            for record in result:
                description = record["description"]
                if node_name in description and property_name in description:
                    return True
                else:
                    return False
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("%s raised an error: \n %s", query, exception)
            raise


if __name__ == "__main__":
    CLIENT_DATA_TEST = "{'ip_address': '127.0.0.1', 'connection_to_port': '1883', 'current_time': '1635015162'}"
    CONNECTION_DATA_TEST = "{'status': 'active', 'current_time': '1635015162', 'name': 'mqtt-explorer-0a61e6f1'}"
    BROKER_DATA_TEST = "{'listener_port': '1883', 'version': '1.6.9'}"
    NEO4J_URI = "bolt://localhost:30687"
    NEO4J_USER = "neo4j"
    NEO4J_PASS = "gh1KLaqw"
    neo4j_driver = Neo4jDatabaseAccess(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    if not neo4j_driver.check_if_node_exists("Client", "ip_address", "127.0.0.1"):
        neo4j_driver.create_client(CLIENT_DATA_TEST)
    if not neo4j_driver.check_if_constraint_exists("Client", "ip_address"):
        neo4j_driver.create_unique_property_constraint("Client", "ip_address")
    neo4j_driver.close()

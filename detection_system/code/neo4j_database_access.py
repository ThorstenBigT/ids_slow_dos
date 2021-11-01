"""[summary]
"""
import logging

from neo4j import GraphDatabase
from beartype import beartype

class Neo4jDatabaseAccess:
    """[summary]
    """

    def __init__(self, uri, user, password):
        """[summary]

        Args:
            uri ([type]): [description]
            user ([type]): [description]
            password ([type]): [description]
        """
  
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """[summary]
        """
        self.driver.close()

    @beartype
    def create_client(self, client_json: dict):
        """[summary]

        Args:
            text ([type]): [description]
            message ([type]): [description]

        Returns:
            [type]: [description]
        """
  
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_client, client_json)
            for record in result:
                print("Created client node: {client}".format(
                    client=client_json['ip_address'])
 
    @staticmethod
    def _create_and_return_client(transaction, client_json):


        query = (
            "CREATE (c1:Client { $property_name: $ }) "
            "RETURN c1"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": record["p1"]["name"], "p2": record["p2"]["name"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


if __name__ == "__main__":
    CLIENT_DATA_TEST = {'ip_address': '127.0.0.1', 'connection_to_port': '1883', 'current_time': '1635015162'}
    CONNECTION_DATA_TEST = {'status': 'active', 'current_time': '1635015162', 'name': 'mqtt-explorer-0a61e6f1'}
    BROKER_DATA_TEST = {'listener_port': '1883', 'version': '1.6.9'}
    NEO4J_URI = "bolt://localhost:30687"
    NEO4J_USER = "neo4j"
    NEO4J_PASS = "gh1KLaqw"
    neo4j_driver = Neo4jDatabaseAccess(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
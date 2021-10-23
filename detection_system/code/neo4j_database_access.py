"""[summary]
"""
from neo4j import GraphDatabase

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

    def print_greeting(self, message):
        """[summary]

        Args:
            message ([type]): [description]
        """
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(text, message):
        """[summary]

        Args:
            text ([type]): [description]
            message ([type]): [description]

        Returns:
            [type]: [description]
        """
        result = text.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


if __name__ == "__main__":
    greeter = Neo4jDatabaseAccess("bolt://localhost:30687", "neo4j", "gh1KLaqw")
    greeter.print_greeting("hello, world")
    greeter.close()

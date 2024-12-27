from neo4j import GraphDatabase
from typing import Optional

from Logger import Logger


class Neo4jOpr:
    """
    A class to manage the connection to the Neo4j database.
    """

    _instance = None
   # NEO4J_HOST = "localhost"
    # NEO4J_PORT = "7687"
    # NEO4J_USER = 'neo4j'
    # NEO4J_PASSWORD = "qwerty"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Neo4jOpr, cls).__new__(cls)
        return cls._instance

    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "qwerty"):
        """
        Initializes the connection to the Neo4j database.
        :param uri: URI of the Neo4j database (e.g., "bolt://localhost:7687")
        :param user: Username for authentication
        :param password: Password for authentication
        """
        self._database = "bron"
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Set the flag to True once initialized
            self._uri = uri
            self._user = user
            self._password = password
            self._driver: Optional[GraphDatabase.Driver] = None
            self.logger = Logger().get_logger()

    def close(self):
        """
        Closes the connection to the Neo4j database.
        """
        if self._driver:
            self._driver.close()
            self.logger.info("Connection closed.")
        else:
            self.logger.debug("No active connection to close.")

    def query(self, query: str, parameters: Optional[dict] = None):
        if self._driver is None:
            self.logger.exception("Connection not established.")
            raise Exception("Connection not established.")
        try:
            with self._driver.session(database=self._database) as session:
                # Log the query and parameters for debugging
                self.logger.debug(f"Running query: {query} with parameters: {parameters}")

                # Run the query and store the result
                result = session.run(query, parameters or {})

                # Check if the result is empty or contains data
                result_list = [record for record in result]
                if not result_list:
                    self.logger.info(f"Query returned no results: {query}")
                else:
                    self.logger.info(f"Query returned {len(result_list)} results.")

                return result_list
        except Exception as e:
            # Log any exceptions that occur during query execution
            self.logger.exception(f"An error occurred while executing the query: {e}")
            raise

    def connect(self):
        """
        Establishes a connection to the Neo4j database.
        """
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
                self.logger.info("Connection successful!")
                print("Connection successful!")
            except Exception as e:
                self.logger.debug(f"Failed to connect to Neo4j: {e}")
                print(f"Failed to connect to Neo4j: {e}")
                self._driver = None  # Explicitly set it to None if connection fails
                self.logger.exception("Problem with connection")
                raise Exception("Problem with connection")
        else:
            self.logger.info("Already connected.")
            print("Already connected.")

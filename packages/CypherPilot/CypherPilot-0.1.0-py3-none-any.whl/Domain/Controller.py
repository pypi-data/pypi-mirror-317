from Domain.Extractor import *
from DataAccess.Neo4jOpr import Neo4jOpr
from Domain.QueryBuilder import QueryBuilder
from Domain.Repository import Repository
from Logger import Logger


class Controller:
    """
    This class serves as a controller that interacts with various components like the database operator
    (Neo4jOpr), the query builder (QueryBuilder), the data extractor (Exctractor), and the repository (Repository).
    It handles operations such as initializing the database connection,
    querying data, saving data to the repository, and extracting data to CSV.
    """
    #instead of hardcoded query, for easily changes
    NodesQuery="CALL db.labels()"
    RelationsQuery="CALL db.relationshipTypes()"

    def __init__(self, uri, user, password):
        """
        This is the constructor for the Controller class. It initializes instances of Exctractor,
         Neo4jOpr, QueryBuilder, and Repository for managing the database connection and data processing.
        :param uri:(str) The URI for the Neo4j database
        :param user: (str) The username for authentication
        :param password:(str) The password for authentication
        """
        self.exctractor = Exctractor()
        self.dbopr = Neo4jOpr(uri,user,password)
        self.queryBuilder = QueryBuilder()
        if not hasattr(Controller, "_repo"):
            Controller._repo = Repository()
        self.repo = Controller._repo
        self.logger = Logger().get_logger()

    def initialize_DB(self):
        """
        This method initializes the database connection by calling the connect() method of the Neo4jOpr class.
         It logs the success or failure of the connection.
        """
        self.logger.info("Initializing database connection...")
        try:
            self.dbopr.connect()
            self.logger.info("Database connection established.")
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise

    def get_by_param(self, dict):
        """
        This method retrieves data based on the parameters in the dict.
        It uses the QueryBuilder to construct the query and the Neo4jOpr class to execute it.
        If the database connection is not established, it attempts to reconnect.
        :param dict:A dictionary containing parameters for the query. It must include the necessary information to build the query using QueryBuilder.
        :return: The result of the query execution.
        """
        try:
            if self.dbopr._driver is None:
                self.initialize_DB() # Attempt to connect
                if self.dbopr._driver is None:
                    self.logger.exception("Connection not established.")
                    raise Exception("Connection not established.")
            query = self.queryBuilder.get_related_nodes(dict)
            result = self.dbopr.query(query)
            return result
        except Exception as e:
            self.logger.exception(f"Error in getbyparam: {e}")
            raise e

    def to_CSV(self,dict):
        """
        This method writes the data to a CSV file. It retrieves the data from the repository
        and then uses the Exctractor class to write the data to a CSV file.
        :param dict:A dictionary containing the necessary information for CSV extraction
        """
        name=dict["name"]
        if "source_columns" in dict:
            source_columns = dict["source_columns"]
        if "target_columns" in dict:
            target_columns = dict["target_columns"]
            self.logger.debug(f"Writing data to CSV for: {name}, Columns: {source_columns} -> {target_columns}")
        data = self.get_data_by_filter("data", name)
        try:
            self.exctractor.write_to_csv(data, dict)
            self.logger.info(f"Data successfully written to CSV: {name}.")
        except Exception as e:
            self.logger.error(f"Failed to write data to CSV: {e}")
            raise

    def save_data_repository(self, name, results):
        """
        This method saves the results of a query into the repository. It calls the save_date_from_query() method
        from the Repository class to store the data.
        :param name:(str) The name of the query or data to be stored in the repository.
        :param results:(list) The results of the query to be saved.
        """
        self.logger.debug(f"Saving {len(results)} records to repository with name: {name}")
        self.repo.save_date_from_query(name, results, len(results))
        self.logger.info(f"Successfully saved {len(results)} records to repository.")

    def get_data_by_filter(self, filter, value):
        """
        This method retrieves data from the repository using a specific filter.
        It calls the get_data_by_filter() method of the Repository class.
        :param filter:(str) The filter criteria to query the repository
        :param value: (str) The value to filter the data by.
        :return:The data retrieved from the repository based on the filter.
        """
        self.logger.debug(f"Fetching data with filter: {filter} = {value}")
        data = self.repo.get_data_by_filter(filter, value)
        return data

    def get_relations(self):
        """
        This method retrieves the types of relationships from the
        Neo4j database by executing  query through the Neo4jOpr class.
        :return:The result of the query, the relationship types in the database.
        """
        try:
            if self.dbopr._driver is None:
                self.dbopr.connect()  # Attempt to connect
                if self.dbopr._driver is None:
                    self.logger.exception("Connection not established.")
                    raise Exception("Connection not established.")
            result = self.dbopr.query(self.RelationsQuery)
            return result
        except Exception as e:
            self.logger.exception(f"Error in get relations: {e}")
            raise e

    def get_nodes_labels(self):
        """
        This method retrieves the labels of nodes from the
        Neo4j database by executing query through the Neo4jOpr class.
        :return:The result of the query, the node labels in the database.
        """
        try:
            if self.dbopr._driver is None:
                self.dbopr.connect()  # Attempt to connect
                if self.dbopr._driver is None:
                    self.logger.exception("Connection not established.")
                    raise Exception("Connection not established.")
            result = self.dbopr.query(self.NodesQuery)
            return result
        except Exception as e:
            self.logger.exception(f"Error in get nodes labels: {e}")
            raise e

    def get_data_properties(self,nodes):
        dict_of_properties = {}
        for node in nodes:
            query = self.queryBuilder.get_data_properties(node)
            results = self.dbopr.query(query)
            dict_of_properties[node] = results
        return dict_of_properties


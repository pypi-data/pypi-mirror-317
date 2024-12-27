from Logger import Logger


class QueryBuilder:
    """
    The QueryBuilder class is responsible for constructing Neo4j Cypher queries based on a set of input parameters.
    It dynamically builds queries to find related nodes, their paths, and any specific constraints.
    """

    def __init__(self):
        """
        This is the constructor for the QueryBuilder class. It initializes the query attribute as an empty string and sets up the logger for logging activities within the class.
        """
        self.query = ""
        self.logger = Logger().get_logger()

    def get_related_nodes(self, dict):
        """
         This method constructs a Cypher query to find related nodes in a Neo4j database based on the input parameters
         provided in the dict. It supports finding related nodes with a specific path length,
         filtering by node labels, and applying a limit on the number of results.
         The query also supports the option to fetch paths between nodes.
        :param dict: (dict) A dictionary containing various parameters for building the query.
        :return:(str) The Cypher query string generated based on the input parameters.
        """
        self.logger.debug("Entering get_related_nodes method.")
        self.query=""
        # Log the incoming parameters
        self.logger.debug(f"Input parameters: {dict}")

        # Initialize the query
        self.query += f"MATCH (startNode:{dict['startNode']} )"
        self.logger.debug(f"Initial query: {self.query}")

        if dict["asapath"] == 'y':
            # Match the related nodes and paths
            self.query += f" MATCH path = (startNode)-[*1..{dict['numberoflayers']}]->(relatedNode) "
            self.logger.debug(f"Path matching with number of layers {dict['numberoflayers']} added to query.")
        else:
            if len(dict["relatedlabels"])>=1:
                self.query += f" MATCH (startNode)-[*1..{dict['numberoflayers']}]-(relatedNode) "
                self.logger.debug(f"Path matching with {dict['numberoflayers']} layers added to query.")

        # If there are related labels, create the WHERE condition
        if "relatedlabels" in dict and len(dict["relatedlabels"])>=1:
            self.query += " WHERE "
            self.logger.debug("Adding related labels to WHERE condition.")
            for i in range(len(dict["relatedlabels"])):
                self.query += f"(relatedNode:{dict['relatedlabels'][i]})"
                if i != len(dict["relatedlabels"]) - 1:
                    self.query += " OR "
            self.logger.debug(f"Updated query with related labels: {self.query}")

        # Use the WITH clause to pass the path and related information
        if dict["asapath"] == 'y':
            self.query+="WITH path, "
            self.query +="startNode.original_id AS start_id, relatedNode.original_id AS end_id,"
            self.query += "nodes(path) AS path_nodes, "  # Include nodes in the path
            self.query += "[node IN nodes(path) | node.original_id] AS original_ids, "  # Include node IDs
            self.query += "[node IN nodes(path) | labels(node)] AS node_labels"  # Include node labels

            self.query+=" WITH path_nodes, start_id, end_id, original_ids, node_labels, REDUCE(s = [],label IN node_labels | CASE WHEN label IN s THEN s ELSE s + [label] END) AS unique_labels "
            self.query+= "WHERE SIZE(unique_labels) = SIZE(node_labels) "
            # Return distinct related nodes and path details
            self.query+="WITH DISTINCT start_id, end_id, path_nodes"
            self.query += " RETURN DISTINCT path_nodes, [node IN path_nodes | node.original_id] AS original_ids, [node IN path_nodes | labels(node)] AS node_labels"
            self.logger.debug("Added path details to query with path_nodes, original_ids, node_labels.")
        else:
            self.query += " RETURN DISTINCT *"

            self.logger.debug("Added return statement for startNode and relatedNode.")

        #add limit for wanted number of records
        if 'limit' in dict:
            limit = int(dict["limit"])
            self.query += f" LIMIT {limit}"
            self.logger.debug(f"Limit of {limit} added to query.")

        # Log the final query
        self.logger.debug(f"Final query: {self.query}")

        return self.query

    def get_data_properties(self, node):
        self.query=f" MATCH(n: {node}) UNWIND keys(n) AS propertyKey RETURN DISTINCT propertyKey ORDER BY propertyKey"
        return self.query

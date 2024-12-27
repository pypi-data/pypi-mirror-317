from Logger import Logger


class Repository:
    """
    This class serves as a repository to store query data and its corresponding aggregation results.
    It manages the data in two separate maps: one for query data (queryDataMap) and one for aggregation results (queryAggregationMap).
    The class provides methods to save data and retrieve it based on specific filters.
    """
    def __init__(self):
        """
        This is the constructor for the Repository class. It initializes two maps: queryDataMap for storing the query data and queryAggregationMap for storing the corresponding aggregation results.
        Additionally, it initializes the logger for logging activities within the class.
        """
        self.queryDataMap = {}
        self.queryAggregationMap = {}
        self.logger = Logger().get_logger()

    def save_date_from_query(self, name, data, agg):
        """
        This method saves the query data and its aggregation under a specified name.
        The data is stored in queryDataMap, and the aggregation is stored in queryAggregationMap.
        :param name: (str) The name of the query, used as the key to store the data and aggregation in the maps.
        :param data: (list) The data retrieved from the query, to be saved in queryDataMap.
        :param agg: (int) The aggregation results of the query, to be saved in queryAggregationMap.
        :return:
        """
        self.logger.debug(f"Entering save_date_from_query method with name: {name}")

        try:
            self.queryDataMap[name] = data
            self.queryAggregationMap[name] = agg
            self.logger.info(f"Saved data and aggregation for query: {name}")
        except Exception as e:
            self.logger.exception(f"Error while saving data and aggregation for {name}: {str(e)}")
            raise

    def get_data_by_filter(self, filter, value):
        """
         This method retrieves data from the repository based on a filter and a value.
         The method supports two filters: "data" (to get only the query data) and "agg" (to get only the aggregation).
         If no filter is provided, both data and aggregation are returned.
        :param filter: (str) The filter used to determine whether to return "data", "agg", or both. If None, both data and aggregation are returned.
        :param value:(str) The key used to look up data and aggregation in the repository.
        :return:The query data and/or aggregation based on the filter.
        """
        self.logger.debug(f"Entering get_data_by_filter method with filter: {filter}, value: {value}")

        # Check if the requested value exists in the repository
        if value not in self.queryDataMap or self.queryDataMap[value] is None:
            self.logger.warning(f"Data not found for value: {value}")
            self.logger.exception(f"Not found {value} as a former query")
            raise Exception(f"Data not found for {value}")

        if filter is None:
            self.logger.debug(f"Returning both data and aggregation for {value}")
            return [self.queryDataMap[value], self.queryAggregationMap[value]]

        if filter == "data":
            self.logger.debug(f"Returning only data for {value}")
            return self.queryDataMap[value]

        if filter == "agg":
            self.logger.debug(f"Returning only aggregation for {value}")
            return self.queryAggregationMap[value]

        self.logger.warning(f"Invalid filter provided: {filter}")
        raise Exception(f"Invalid filter: {filter}")

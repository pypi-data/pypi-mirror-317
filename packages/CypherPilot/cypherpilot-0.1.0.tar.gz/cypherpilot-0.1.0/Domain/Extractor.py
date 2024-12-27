import csv
from Logger import Logger


class Exctractor:
    """
    The Exctractor class is responsible for writing data to CSV files, including nodes, edges, and paths from a Neo4j database. It provides methods
    to handle different data formats and ensure data consistency when writing to the CSV file.
    """

    def __init__(self):
        """
        This is the constructor for the Exctractor class.
        It initializes a logger to record activities within the class.
        """
        self.logger = Logger().get_logger()

    def write_to_csv(self, data,dict):
        """
        This method writes the provided data to a CSV file based on the configuration in the dict parameter. It handles different types of data (such as nodes, edges, or paths)
        and generates a CSV file based on the provided columns and other flags.
        :param data:  (list) A list of data records to be written to the CSV file. These can include nodes, edges, or paths.
        :param dict:(dict) A dictionary that contains configuration details for writing the CSV
        """
        name=dict["name"]
        if "source_columns" in dict:
            source_columns = dict["source_columns"]
        if "target_columns" in dict:
            target_columns = dict["target_columns"]
        # Ensure the file name ends with '.csv'
        name = f"{name}.csv"
        with open(name, 'w', newline='', encoding='utf-8') as csvfile:
            if dict["name"]=="edges" or dict["name"]=="nodes":
                self.scheme_function(dict, csvfile, data)
                return

            # Write the rows

            row = {}
            try:
                y = data[0]["path_nodes"]
                self.csv_path(data,source_columns,target_columns,row,dict["flag_full_path"],csvfile)
                return
            except Exception as e:

                source_columns = [f"{col}_startNode" for col in source_columns]
                target_columns = [f"{col}_relatedNode" for col in target_columns]

                # Combine source and target columns for the header
                unique_flag=True
                fieldnames =[]
                duplicate ={}
                for record in data:
                    # Initialize row as an empty dictionary for each record
                    row = {}
                    # Get the startNode and relatedNode properties
                    start_prop = record["startNode"]._properties
                    #------------------------------------------
                    if len(target_columns)>=1:
                        related_prop = record["relatedNode"]._properties
                    is_duplicate = duplicate.get(start_prop['original_id'],False)
                    if is_duplicate:
                        continue
                    duplicate[start_prop['original_id']] = True
                    self.write_col(source_columns,start_prop,"_startNode",fieldnames,row,unique_flag)
                    # Populate the row for the target columns (relatedNode)
                    if len(target_columns)>=1:
                        self.write_col(target_columns,related_prop,"_relatedNode",fieldnames,row,unique_flag)

                    # Write the header once
                    if unique_flag:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        unique_flag = False

                    # Write the row to the CSV file
                    writer.writerow(row)

        self.logger.info(f"Data written to {name}")

        self.logger.info(f"CSV file '{name}' has been created successfully.")


    def csv_path(self,data,source_columns,target_columns,row,flag,csvfile):
        """
        This helper method is used to handle the specific case when data includes paths.
        It processes the records to extract path-related data and writes it to the CSV file.
        :param data:(list) A list of path-related data to be written.
        :param source_columns: (list) A list of source columns to be written to the CSV file.
        :param target_columns: (list) A list of target columns to be written to the CSV file.
        :param row:(dict) A dictionary that stores the current row being written to the CSV file
        :param flag: A flag indicating whether to include the full path.
        :param csvfile(file object): The file object representing the CSV file where the data will be written.
        :return:
        """
        # Create a CSV writer object
        flagoffields=True
        duplicates={}
        for record in data:
            raw = record[0]
            original_id=record[1]
            data_type = record[2]
            if flagoffields:
                flagoffields=False
                fieldnames= self.headers(source_columns,target_columns,data_type,flag)
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    # Write the header row
                writer.writeheader()
            first_item = raw[0]._properties  # First element
            last_item = raw[len(raw) - 1]._properties  # Last element
            is_duplicate=self.remove_duplicate(first_item,last_item,duplicates)
            if is_duplicate:
                continue
            self.write_record(row,source_columns,target_columns,first_item,last_item,raw,flag)
            writer.writerow(row)
            # Write the row to the CSV file

    def headers(self, source_columns, target_columns, data_type,flag):
        """
        This helper method generates the headers (column names) for the CSV file based on the source and target columns and the data type.
        :param source_columns: (list) A list of source columns to be written to the CSV file.
        :param target_columns: (list) A list of target columns to be written to the CSV file.
        :param data_type: (list) A list of data types for the nodes involved in the relationship
        :param flag:(bool) A flag indicating whether to include the full path.
        :return:(list) A list of column names to be used as headers in the CSV file.
        """
        fieldsnames=[]
        for col in source_columns:
            # Extract the base column name without '_relatedNode'
            col_base = col.replace('_startNode', '')
            key = [f"{col_base}_{data_type[0][0]}"]
            if key not in fieldsnames:
                fieldsnames += key
        if flag:
            for i in range(1,len(data_type)-1):
                key = [f"original_id_{data_type[i][0]}"]
                if key not in fieldsnames:
                    fieldsnames+=key
        for col in target_columns:
            # Extract the base column name without '_relatedNode'
            col_base = col.replace('_relatedNode', '')
            key = [f"{col_base}_{data_type[len(data_type) - 1][0]}"]
            if key not in fieldsnames:
                fieldsnames += key
        return fieldsnames

    def remove_duplicate(self, first_item, last_item, duplicates):
        """
         This helper method checks if the given records (first_item and last_item) are duplicates based on their original_id. If both records have been seen before, it skips writing them.
        :param first_item: (dict) The properties of the first node in the path.
        :param last_item: (dict) The properties of the last node in the path.
        :param duplicates:(dict) A dictionary used to track seen original_ids
        :return:True if the records are duplicates, False otherwise.
        """
        x = duplicates.get(first_item['original_id'], False)
        if not x:
            duplicates[first_item['original_id']] = True
        y = duplicates.get(last_item['original_id'], False)
        if not y:
            duplicates[last_item['original_id']] = True
        if x and y:
            return True
        return False

    def write_record(self, row, source_columns, target_columns, first_item, last_item, raw,flag):
        """
        This helper method writes the data for a single record into the row dictionary, which will be written to the CSV file.
        :param row:(dict) The dictionary storing the current record data.
        :param source_columns:(list) A list of source column names for the startNode.
        :param target_columns: (list) A list of target column names for the relatedNode.
        :param first_item: (dict) The properties of the first node in the path.
        :param last_item: (dict) The properties of the last node in the path
        :param raw: (list) The raw data representing the path.
        :param flag:
        :return: (bool) A flag indicating whether to include the full path.
        """

        for col in source_columns:
            col_base = col.replace('_startNode', '')
            row[f"{col_base}_{first_item['datatype']}"] = first_item.get(col_base,None)  # Use get() to handle missing keys
        if flag:
            for i in range(1, len(raw) - 1):
                tmpdict = raw[i]._properties
                key = f"{'original_id'}_{tmpdict['datatype']}"
                row[key] = tmpdict['original_id']
        for col in target_columns:
            col_base = col.replace('_relatedNode', '')
            row[f"{col_base}_{last_item['datatype']}"] = last_item.get(col_base, None)

    def write_col(self,columns, prop, param, fieldnames,row,flag):
        """
        This helper method writes data for individual columns (either for the source or target node) into the row dictionary, ensuring that the column names are unique.
        :param columns: (list) A list of column names to write to the CSV.
        :param prop:(dict) The properties of the current node (startNode or relatedNode).
        :param param: (str) A string used to differentiate the source and target node columns.
        :param fieldnames: (list) A list of column names to be used as headers.
        :param row:(dict) A dictionary storing the current record data.
        :param flag: (bool) A flag indicating whether to include the full path.
        :return:
        """
        # Populate the row for the source columns (startNode)
        for col in columns:
            col_base = col.replace(param, f"_{prop['datatype']}")
            col_clean = col.replace(param, '')
            row[col_base] = prop.get(col_clean, None)  # Handle missing keys

            # Append col_base to fieldnames only once
            if flag:
                fieldnames.append(col_base)

    def scheme_function(self, dict,csvfile,data):
        """
        This method is responsible for handling data when it pertains to nodes or edges (not paths). It writes the relevant properties (such as node labels or relationship types) to the CSV file.
        :param dict:(dict) A dictionary containing configuration details for the CSV file.
        :param csvfile:(file object)The file object representing the CSV file where the data will be written.
        :param data:(list)A list of node or edge data to be written.
        """
        fieldnames = []
        fieldnames.append("information")
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in data:
            row = {}
            if "nodes" in dict:
                row["information"] = record["label"]
            else:
                row["information"] = record["relationshipType"]
            writer.writerow(row)


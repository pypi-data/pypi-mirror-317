from Presentation.Gate import Gate
import Service

from Service import  Service


def printingCPE(record):
    print(f"Element ID: {record.get('elementid', 'N/A')}")
    print(f"Label: {record.get('labels', 'N/A')}")
    print(f"ID: {record.get('id', 'N/A')}")
    print(f"Original ID: {record.get('original_id', 'N/A')}")
    print(f"Vendor: {record.get('metadata_vendor', 'N/A')}")
    print(f"Product: {record.get('metadata_product', 'N/A')}")
    print(f"Version: {record.get('metadata_version', 'N/A')}")

    # Print other properties for 'cpe'
    for key, value in record.items():
        if key not in ['elementid', 'labels', 'id', 'original_id', 'metadata_vendor', 'metadata_product',
                       'metadata_version']:
            print(f"{key}: {value}")


def printiningCAPEC(record):
    print(f"Element ID: {record.get('elementid', 'N/A')}")
    print(f"Label: {record.get('label', 'N/A')}")
    print(f"Name: {record.get('name', 'N/A')}")
    print(f"Short Description: {record.get('metadata_short_description', 'N/A')}")
    print(f"Typical Severity: {record.get('metadata_typical_severity', 'N/A')}")
    print(f"Likelihood of Attack: {record.get('metadata_likelihood_of_attack', 'N/A')}")
    print(f"Consequences: {record.get('metadata_consequences', 'N/A')}")
    print(f"Skills Required: {record.get('metadata_skills_required', 'N/A')}")

    # Print other properties for 'capec'
    for key, value in record.items():
        if key not in ['label', 'elementid', 'name', 'metadata_short_description',
                       'metadata_typical_severity', 'metadata_likelihood_of_attack',
                       'metadata_consequences', 'metadata_skills_required']:
            print(f"{key}: {value}")


def printingCWE(record):
    print(f"Element ID: {record.get('elementid', 'N/A')}")
    print(f"Label: {record.get('label', 'N/A')}")

    # Print properties for 'cwe'
    for key, value in record.items():
        if key not in ['label', 'elementid']:
            print(f"{key}: {value}")


def printingCVE(record):
    print(f"Label: {record.get('label', 'N/A')}")
    print(f"Element ID: {record.get('elementid', 'N/A')}")

    # Print properties for 'cve'
    for key, value in record.items():
        if key not in ['label', 'elementid']:
            print(f"{key}: {value}")


class Presentation:

    def __init__(self):
        self.gate = Gate("bolt://localhost:7687","neo4j","qwerty")

    def initDB(self):
        uri = input("what is the wanted uri")
        user = input("what is the user")
        password = input("what is the password if any, if not - enter 0")
        self.db = self.service.initDB()



    def Demo_pres(self):
        #param = ["cve","cwe",["original_id", "metadata_description"],["original_id", "name"]]

        while True:
            print("\nMenu:")
            print("1. direct query")
            print("2. data property query")
            print("3. path query")
            print("4. all nodes")
            print("5. all edges")

            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                param = ["cve","cwe",["original_id", "metadata_description"],["original_id", "name"],False,True]
                param = ["cve","cpe",["original_id"],["metadata_vendor","metadata_product","original_id"],False,"sample1",10000]
                self.gate.query(param)
                #self.gate.direct_query(param)

            elif choice == "2":
                param = ["cwe",None,["original_id","_key"],[],False,"sample2",10000]
                self.gate.query(param)
                #self.gate.path_query(param)
            elif choice == "3":
                #param= ["cwe","cpe",["original_id","metadata_applicable_platform"],["original_id","metadata_vendor"],True,100]
                param= ["technique","cve",["original_id","metadata_description"],["original_id","metadata_description"],True,"sample3",10000]
                #param= ["cwe","cpe",["original_id"],["original_id"],True]

                self.gate.query(param)
            elif choice == "4":
                param = []
                param.append("nodes")
                self.gate.query(param)
            elif choice == "5":
                param=[]
                param.append("edges")
                self.gate.query(param)

            else:
                print("Invalid choice, please choose a number between 1 and 4.")


    def finalPrint(self, parsed_data):
        if parsed_data[0]=="path":
            for i in range(1,len(parsed_data)):
                print(parsed_data[i])
            return
        for record in parsed_data:
            print("----- Record -----")

            # Check the 'datatype' to determine if it's 'cve', 'cwe', 'capec', or 'cpe'
            datatype = record.get('datatype', 'N/A')

            # Print 'cve' data in the first format
            if datatype == 'cve':
                printingCVE(record)

            # Print 'cwe' data in the new format
            elif datatype == 'cwe':
                printingCWE(record)

            # Print 'capec' data in the new format
            elif datatype == 'capec':
                printiningCAPEC(record)

            # Print 'cpe' data in the new format
            elif datatype == 'cpe':
                printingCPE(record)

            else:
                print(f"Unsupported datatype: {datatype}")

            print("\n")

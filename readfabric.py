from azure.identity import InteractiveBrowserCredential
import struct
from itertools import chain, repeat
import pyodbc
from dotenv import load_dotenv
import os

credential = InteractiveBrowserCredential()

load_dotenv()

sql_endpoint = os.environ.get("sql_endpoint")
database = "lakehousedemo" # copy and paste the name of the Lakehouse or Warehouse you want to connect to

connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={sql_endpoint},1433;Database=f{database};Encrypt=Yes;TrustServerCertificate=No"

# prepare the access token

token_object = credential.get_token("https://database.windows.net//.default") # Retrieve an access token valid to connect to SQL databases
token_as_bytes = bytes(token_object.token, "UTF-8") # Convert the token to a UTF-8 byte string
encoded_bytes = bytes(chain.from_iterable(zip(token_as_bytes, repeat(0)))) # Encode the bytes to a Windows byte string
token_bytes = struct.pack("<i", len(encoded_bytes)) + encoded_bytes # Package the token into a bytes object
attrs_before = {1256: token_bytes}  # Attribute pointing to SQL_COPT_SS_ACCESS_TOKEN to pass access token to the driver

# build the connection

connection = pyodbc.connect(connection_string, attrs_before=attrs_before)

cursor = connection.cursor()
cursor.execute("SELECT CustomerName, Email FROM [lakehousedemo].[dbo].[dimcustomer_gold] where CustomerID in (12315,545,665,1163,290)")
rows = cursor.fetchall()
print(rows) # this will print all the tables available in the lakehouse or warehouse

cursor.close()
connection.close()
# from azure.identity import InteractiveBrowserCredential
# import struct
# from itertools import chain, repeat
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

client_id=os.environ.get("client_id")
client_secret=os.environ.get("client_secret")
tenant_id=os.environ.get("tenant_id")

sql_endpoint = os.environ.get("sql_endpoint")
database = "lakehousedemo"
service_principal_id = f"{client_id}@{tenant_id}"

conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={sql_endpoint};"
    f"DATABASE={database};"
    f"UID={service_principal_id};"
    f"PWD={client_secret};"
    f"Authentication=ActiveDirectoryServicePrincipal;"
    f"Encrypt=yes"
)
# print connection string
# print (conn_str)

# Connect to the SQL Server
conn = pyodbc.connect(conn_str)

# Now you can use `conn` to interact with your database
# Create a cursor
cursor = conn.cursor()

# Define your query
query = "SELECT CustomerName, Email FROM [lakehousedemo].[dbo].[dimcustomer_gold] where CustomerID in (12315,545,665,1163,290);"

# Execute the query
cursor.execute(query)

# Fetch all rows from the last executed statement
rows = cursor.fetchall()

# Print all rows
for row in rows:
    print(row)
import sys
import subprocess
from termcolor import colored

# Function to fetch data from the database using subprocess and --login-path
def fetch_data_from_db(database_name, table_name, order_column):
    sql_command = f"SELECT * FROM {table_name} ORDER BY {order_column} ASC"

    cmd = [
        "mysql",
        "--login-path=client",
        "-e",
        sql_command,
        database_name
    ]

    subprocess.run(cmd, check=True)

sys.stdout.write(colored("Enter the database name: ", 'yellow'))
sys.stdout.flush()  # Make sure the output is immediately shown
database_name = input()

sys.stdout.write(colored("Enter the table name: ", 'yellow'))
sys.stdout.flush()
table_name = input()

sys.stdout.write(colored("Enter the column name to order by: ", 'yellow'))
sys.stdout.flush()
order_column = input()

fetch_data_from_db(database_name, table_name, order_column)

print(colored(f"Data from table {table_name} in {database_name} fetched and ordered by {order_column} successfully.", 'red'))

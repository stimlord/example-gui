import subprocess
import sys
from termcolor import colored

# Function to run SQL commands using subprocess and --login-path
def run_sql_command(sql_command, database_name):
    cmd = [
        "mysql",
        "--login-path=client",
        "-e",
        sql_command,
        database_name
    ]
    subprocess.run(cmd, check=True)

# Get database name from the user
sys.stdout.write(colored("Enter the database name: ", 'yellow'))
sys.stdout.flush()  # Make sure the output is immediately shown
database = input()

# Get table name from the user
sys.stdout.write(colored("Enter the table name: ", 'yellow'))
sys.stdout.flush()  # Make sure the output is immediately shown
table_name = input()

# Get column name for the WHERE clause
sys.stdout.write(colored("Enter the column name: ", 'yellow'))
sys.stdout.flush()  # Make sure the output is immediately shown
column_name = input()

# Prompt the user for the value to compare
sys.stdout.write(colored(f"Enter the value, delete -->> {column_name} where > INPUT: ", 'yellow'))
sys.stdout.flush()  # Make sure the output is immediately shown
input_value = input()

# Delete rows based on the provided column and value
delete_query = f"DELETE FROM {table_name} WHERE {column_name} > {input_value}"

run_sql_command(delete_query, database)

print(colored(f'Deleted rows from table {table_name} in database {database} where {column_name} > {input_value}.', 'red'))

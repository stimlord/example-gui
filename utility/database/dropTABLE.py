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

# Function to delete a table
def delete_table(database_name, table_name):
    # SQL command to delete table
    sql_command = f"DROP TABLE IF EXISTS {table_name};"
    run_sql_command(sql_command, database_name)

# Get database name from the user
sys.stdout.write(colored("Enter the name of the database: ", 'yellow'))
sys.stdout.flush()  # Make sure the output is immediately shown
database = input()

# Get table name from the user
sys.stdout.write(colored("Enter the name of the table to delete: ", 'yellow'))
sys.stdout.flush()  # Make sure the output is immediately shown
table = input()

delete_table(database, table)
print(colored(f"Table {table} has been deleted from {database}.", 'red'))

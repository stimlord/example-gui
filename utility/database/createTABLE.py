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

# Create table in the specified database with the specified table name
sql_command = f'''
CREATE TABLE IF NOT EXISTS {table_name} (
    
);
'''
run_sql_command(sql_command, database)

print(colored(f'Table {table_name} created successfully in {database}', 'red'))

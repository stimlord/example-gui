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

sys.stdout.write(colored("Enter the database name: ", 'yellow'))
sys.stdout.flush()
database_name = input()

show_tables_query = "SHOW TABLES"
run_sql_command(show_tables_query, database_name)

print(colored(f"List of tables in the database {database_name}:", 'red'))

import sys
import subprocess
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
sys.stdout.flush()  # Make sure the output is immediately shown
database_name = input()

sys.stdout.write(colored("Enter the table name: ", 'yellow'))
sys.stdout.flush()
table = input()

sql_command = f"DESCRIBE {table};"
run_sql_command(sql_command, database_name)

print(colored(f'Description of {table} fetched successfully.', 'red'))

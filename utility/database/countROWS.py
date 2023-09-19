import subprocess
import sys
from termcolor import colored

# Function to run SQL commands using subprocess and --login-path
def run_sql_command(sql_command, database):
    cmd = [
        "mysql",
        "--login-path=client",
        "-e",
        sql_command,
        database
    ]

    # Execute the SQL command and capture the output
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout.strip()

# Function to get approximate row count
def get_approximate_row_count(database, table):
    # SQL command to get approximate row count from information_schema
    sql_command = f"""
    SELECT TABLE_ROWS
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = '{database}'
    AND TABLE_NAME = '{table}';
    """
    result = run_sql_command(sql_command, "information_schema")
    row_count = result.split('\n')[-1]  # Split by newline and take the last value
    return int(row_count)

# Get database name from the user
sys.stdout.write(colored("Enter the database name: ", 'yellow'))
sys.stdout.flush()  # Make sure the output is immediately shown
database = input()

# Get table name from the user
sys.stdout.write(colored("Enter the table name: ", 'yellow'))
sys.stdout.flush()
table = input()

approx_rows = get_approximate_row_count(database, table)
print(colored(f"Approximate number of rows in {table}: {approx_rows}", 'red'))

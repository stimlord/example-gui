import os
import sys
import subprocess
from termcolor import colored

def start_ganache(mnemonic):
    try:
        subprocess.run(["ganache-cli", "--mnemonic", mnemonic])
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    mnemonics = [
        ""
    ]

    print(colored("Select a mnemonic:", 'magenta'))
    for i, mnemonic in enumerate(mnemonics, 1):
        print(f"{i}.", colored(f"{mnemonic}", 'cyan'))

    choice = int(input(colored("Enter the number of the mnemonic you want to use: ", 'yellow')))

    if 0 < choice <= len(mnemonics):
        start_ganache(mnemonics[choice - 1])
    else:
        print("Invalid choice!")

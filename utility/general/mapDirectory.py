import os
import sys
from termcolor import colored

def print_directory_structure(start_directory, ignore_dirs=[], ignore_files=[]):
    for root, dirs, files in os.walk(start_directory):

        # Remove directories from the traversal if they are in the ignore list
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        level = root.replace(start_directory, '').count(os.sep)
        indent = ' ' * 4 * level
        print(colored(f'{indent}{os.path.basename(root)}/', 'cyan'))

        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in ignore_files:
                print(colored(f'{sub_indent}{f}', 'red'))

if __name__ == '__main__':
    sys.stdout.write(colored("Enter the directory path: ", 'yellow'))
    sys.stdout.flush()  # Make sure the output is immediately shown
    directory = input().strip()

    dirs_to_ignore = [".git", "node_modules", "target"]
    files_to_ignore = [".DS_Store", "package-lock.json", "package.json", "Cargo.lock"]
    print_directory_structure(directory, dirs_to_ignore, files_to_ignore)

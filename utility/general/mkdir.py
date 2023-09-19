import os
import sys
import subprocess
from termcolor import colored

BASE_PATH = "/Users/ui3u/example"

def create_directory(name):
    path = os.path.join(BASE_PATH, "ALL_PROJECTS_GO_HERE", name)
    os.makedirs(path, exist_ok=True)
    return path

def update_zshrc_utility(name):
    zshrc_path = os.path.expanduser("~/.zshrc-utility")

    # Read the file line by line
    with open(zshrc_path, 'r') as f:
        lines = f.readlines()

    # Create the new content to be inserted
    new_content = f'''
    elif [[ $current_dir == *"/Users/ui3u/example/ALL_PROJECTS_GO_HERE/{name}"* ]]; then
        cargo run --manifest-path /Users/ui3u/example/ALL_PROJECTS_GO_HERE/{name}/Cargo.toml utility
    '''

    # Find the line starting with 'else' and insert the new content before it
    for i, line in enumerate(lines):
        if line.strip().startswith("else"):
            lines.insert(i, new_content)
            break

    # Write back the modified content
    with open(zshrc_path, 'w') as f:
        f.writelines(lines)


def update_root_cargo_toml(name):
    cargo_toml_path = os.path.join(BASE_PATH, "Cargo.toml")

    with open(cargo_toml_path, 'r') as f:
        lines = f.readlines()

    # Find the start of the members array and insert the new directory there
    for i, line in enumerate(lines):
        if line.strip().startswith("members = ["):
            lines.insert(i+1, f'    "ALL_PROJECTS_GO_HERE/{name}",\n')
            break

    with open(cargo_toml_path, 'w') as f:
        f.writelines(lines)

def create_project_cargo_toml(directory_path):
    content = '''[package]
name = "{name}"
version = "0.1.0"
edition = "2021"

[dependencies]
utility = {{ path = "/Users/ui3u/example/utility" }}
colored = "1.9"
'''

    with open(os.path.join(directory_path, "Cargo.toml"), "w") as f:
        f.write(content.format(name=os.path.basename(directory_path)))

def initialize_rust_project(directory_path):
    result = subprocess.run(["cargo", "init", directory_path], capture_output=True, text=True)

    error_message = "current package believes it's in a workspace when it's not:"

    if error_message not in result.stderr:
        # If there's any other error, print it
        print(result.stderr)

def update_main_rs(directory_path):
    main_rs_content = '''use utility::utility_runner::run_utility;

fn main() {
    run_utility();
}
'''

    main_rs_path = os.path.join(directory_path, "src", "main.rs")

    with open(main_rs_path, 'w') as f:
        f.write(main_rs_content)



def main():
    sys.stdout.write(colored("Enter the Directory Name: ", 'yellow'))
    sys.stdout.flush()
    new_dir_name = input()

    # Check for reserved names
    reserved_names = ["test"]
    if new_dir_name in reserved_names:
        print(colored(f"'{new_dir_name}' is a reserved name in Rust. Please choose a different name.", 'red'))
        return

    directory_path = create_directory(new_dir_name)

    initialize_rust_project(directory_path)  # Initialize Rust project first
    update_main_rs(directory_path)
    update_zshrc_utility(new_dir_name)
    update_root_cargo_toml(new_dir_name)
    create_project_cargo_toml(directory_path)
    print(colored(f"Project {new_dir_name} initialized!", 'red'))
    print(colored("\nReminder: Don't forget to source your file using the command:", 'red'))
    print(colored("source ~/.zshrc-utility", 'red'))


if __name__ == "__main__":
    main()

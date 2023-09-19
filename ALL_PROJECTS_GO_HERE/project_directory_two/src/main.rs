use std::env;
use std::fs::{self, File};
use std::io::{self, Write, BufRead, BufReader};
use std::path::{Path, PathBuf};
use std::process::Command;
use colored::*;
use utility::utility_runner::run_utility;


#[derive(Debug)]
enum ItemType {
    Directory,
    File,
}


fn find_root_directory() -> Option<PathBuf> {
    let mut current_dir = env::current_dir().ok()?;

    loop {
        let cargo_toml_path = current_dir.join("Cargo.toml");
        if cargo_toml_path.exists() {
            return Some(current_dir);
        }

        if !current_dir.pop() {
            break;
        }
    }

    None
}

fn get_ignore_list() -> io::Result<Vec<String>> {
    let root_directory = find_root_directory()
        .ok_or(io::Error::new(io::ErrorKind::NotFound, "Failed to find root directory containing Cargo.toml"))?;

    let ignore_list_path = root_directory.join("ignore_list.txt");

    match File::open(ignore_list_path) {
        Ok(file) => {
            let reader = BufReader::new(file);
            Ok(reader.lines().filter_map(|l| l.ok()).collect())
        },
        Err(e) => {
            println!("{}", format!("Failed to open ignore_list.txt: {:?}", e).red());
            Err(e)
        }
    }
}


fn list_all_items(directory: &Path) -> io::Result<Vec<(String, ItemType)>> {
    let mut items = Vec::new();
    let ignore_list = get_ignore_list()?;

    println!("{}", format!("Reading from directory: {:?}", directory).green());
    println!("{}", "Please select from the given numbers.".magenta());


    for entry in fs::read_dir(directory)? {
        let path = entry?.path();
        let item_name = path.file_name().unwrap().to_string_lossy().to_string();


        if ignore_list.contains(&item_name) {
            continue;
        }

        if path.is_dir() {
            items.push((item_name, ItemType::Directory));
        } else if path.is_file() {
            items.push((item_name, ItemType::File));
        }
    }

    Ok(items)
}

fn execute_file(file_path: &Path) -> io::Result<()> {
    if let Some(extension) = file_path.extension() {
        match extension.to_string_lossy().as_ref() {
            "py" => {
                Command::new("python3")
                    .arg(file_path)
                    .status()?;
            },
            "js" => {
                Command::new("node")
                    .arg(file_path)
                    .status()?;
            },
            "rs" => {
                // Use a temporary directory for Rust compilation
                let tmp_dir = tempfile::tempdir()?;
                let output_file = tmp_dir.path().join(file_path.file_stem().unwrap());

                let compile_status = Command::new("rustc")
                    .arg(file_path)
                    .arg("-o")
                    .arg(&output_file)
                    .status()?;

                if compile_status.success() {
                    Command::new(&output_file)
                        .status()?;
                } else {
                    eprintln!("{}", format!("Failed to compile Rust file: {:?}", file_path).red());
                    return Err(io::Error::new(io::ErrorKind::Other, "Compilation failed"));
                }
            },
            _ => println!("Unsupported file type."),
        }
    }
    Ok(())
}


fn handle_library(_library: &str) {
    match run_utility() {
        Ok(_) => {},  // Do nothing if it's okay
        Err(e) => println!("{}", e.to_string().red()),
    }
}

fn main() {
    println!("{}", "--------------------------------------------------".black());
    let args: Vec<String> = env::args().collect();

    // If the 'utility' argument is provided
    if args.len() > 1 && args[1] == "utility" {
        handle_library("utility");
        return;
    }

    // Check for the 'active' argument
    let current_dir = if args.len() > 1 && args[1] == "active" {
        env::current_dir().unwrap()
    } else {
        find_root_directory().unwrap_or(env::current_dir().unwrap())
    };

    let mut src_dir = current_dir;

    loop {
        let items = list_all_items(&src_dir).unwrap_or_default();

        if items.is_empty() {
            println!("{}", "No items found or all items are ignored.".red());
            break;
        }

        for (i, (name, item_type)) in items.iter().enumerate() {
            match item_type {
                ItemType::Directory => println!("{}. {} (directory)", i + 1, name.cyan()),
                ItemType::File => println!("{}. {} (file)", i + 1, name.blue()),
            }
        }

        print!("{}", "Input Number: ".yellow());
        io::stdout().flush().unwrap();

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();

        let idx: usize = choice.trim().parse().unwrap_or(0);

        if idx == 0 || idx > items.len() {
            println!("{}", "Invalid choice".red());
            break;
        }

        match items[idx - 1].1 {
            ItemType::Directory => {
                src_dir = src_dir.join(&items[idx - 1].0);
            },
            ItemType::File => {
                let file_path = src_dir.join(&items[idx - 1].0);
                match execute_file(&file_path) {
                    Ok(_) => break,
                    Err(e) => println!("{}", format!("Failed to execute file: {}", e).red()),
                }
            }
        }
    }
}

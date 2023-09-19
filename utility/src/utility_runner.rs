use std::io::{self, Write};
use crate::utility::*;
use colored::*;


pub fn run_utility() -> Result<(), Box<dyn std::error::Error>> {
    println!("{}", "--------------------------------------------------".black());

    if std::env::args().len() > 1 && std::env::args().nth(1).unwrap() == "utility" {
        let utility_path = "/Users/ui3u/example/utility";
        let mut dirs = list_directories(utility_path).expect("Failed to list directories");

        // Add an option for using the current directory
        dirs.push(std::env::current_dir()?.display().to_string());

        println!("{}","Select a Directory:".magenta());
        for (i, dir) in dirs.iter().enumerate() {
            println!("{}. {}", i + 1, dir.cyan());
        }

        print!("{}", "Input Number: ".yellow());
        io::stdout().flush().unwrap();

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).expect("Failed to read line");
        let idx: usize = choice.trim().parse().expect("Please input a number");
        if idx == 0 || idx > dirs.len() {
            println!("Invalid choice");
            return Err(Box::new(std::io::Error::new(std::io::ErrorKind::Other, "Invalid directory choice")));
        }

        let chosen_dir = if idx == dirs.len() {
            std::env::current_dir()?.display().to_string()
        } else {
            dirs[idx - 1].clone()
        };

        let scripts = get_scripts_from_directory(&chosen_dir).expect("Failed to get scripts");
        println!("{}", "Choose a script to run:".magenta());
        for (i, script) in scripts.iter().enumerate() {
            println!("{}. {}", i + 1, script.cyan());
        }

        print!("{}", "Input: ".yellow());
        io::stdout().flush().unwrap();

        let mut script_choice = String::new();
        io::stdin().read_line(&mut script_choice).expect("Failed to read line");
        let script_idx: usize = script_choice.trim().parse().expect("Please input a number");
        if script_idx == 0 || script_idx > scripts.len() {
            println!("{}", "Invalid choice".red());
            return Err(Box::new(std::io::Error::new(std::io::ErrorKind::Other, "Invalid script choice")));
        }
        let script_name = &scripts[script_idx - 1];

        run_python_script(&chosen_dir, script_name)?;
    }

    Ok(())
}

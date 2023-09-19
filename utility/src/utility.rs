use std::process::{Command, Stdio};
use std::fs;
use colored::*;
use std::io;



pub fn list_directories(absolute_path: &str) -> io::Result<Vec<String>> {
    let mut directories = Vec::new();
    for entry in fs::read_dir(absolute_path)? {
        let entry = entry?;
        if entry.path().is_dir() && entry.path().file_name().unwrap().to_str().unwrap() != "src" {
            directories.push(entry.path().file_name().unwrap().to_string_lossy().to_string());
        }
    }
    Ok(directories)
}


pub fn get_scripts_from_directory(directory: &str) -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let path = if directory.starts_with("/Users/ui3u") {
        directory.to_string()
    } else {
        format!("/Users/ui3u/example/utility/{}", directory)
    };

    let abs_path = std::fs::canonicalize(&path)?;
    println!("{} {}", "Absolute path being accessed:".green(), abs_path.display().to_string().green());

    let entries = fs::read_dir(&path)?;

    Ok(entries.filter_map(|entry| {
        let path = entry.ok()?.path();
        if path.is_file() && path.extension()?.to_string_lossy() == "py" {
            Some(path.file_name()?.to_string_lossy().to_string())
        } else {
            None
        }
    }).collect())
}


pub fn run_python_script(directory: &str, script_name: &str) -> Result<(), Box<dyn std::error::Error>> {
    // Ensure python3 is available
    if Command::new("python3").arg("--version").stdout(Stdio::null()).stderr(Stdio::null()).status().is_err() {
        return Err(Box::new(std::io::Error::new(std::io::ErrorKind::NotFound, "python3 not found")));
    }

    // Determine the script path based on the directory
    let script_path = if directory.starts_with("/Users/ui3u") {
        format!("{}/{}", directory, script_name)
    } else {
        format!("/Users/ui3u/example/utility/{}/{}", directory, script_name)
    };

    println!("{} {}", "Attempting to run script at path:".green(), script_path.green());

    let status = Command::new("python3")
        .arg(&script_path)
        .status()?;  // Run the script and wait for it to complete

    if !status.success() {
        eprintln!("Python Error: Script execution failed.");
        return Err(Box::new(std::io::Error::new(std::io::ErrorKind::Other, "Python script failed")));
    }

    Ok(())
}

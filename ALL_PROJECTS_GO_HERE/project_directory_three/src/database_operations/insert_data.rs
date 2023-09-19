// This code is used to inset data from our downloadZipMonthly.py
// file to the appropriate database, we used rust because its faster
// than python.
use std::process::Command;

pub fn insert_data() {
    // Open the CSV file.
    let mut rdr = csv::Reader::from_path("/Users/ui3u/zip-processing/CSV/BTCUSDT-trades-2022-01.csv").unwrap();

    let mut values = Vec::new();
    const BATCH_SIZE: usize = 5_000;

    // Begin the transaction.
    start_transaction();

    // Process each record from the CSV.
    for result in rdr.records() {
        match result {
            Ok(record) => {
                if record.len() != 6 {
                    eprintln!("Problematic record at line {}: {:?}", record.position().unwrap().line(), record);
                    continue;
                }

                let is_buyer_maker = if &record[5] == "true" { "1" } else { "0" };
                let value_string = format!(
                    "('{}', '{}', '{}', '{}', '{}', '{}')",
                    &record[0], &record[1], &record[2], &record[3], &record[4], is_buyer_maker
                );
                values.push(value_string);

                if values.len() == BATCH_SIZE {
                    insert_batch(&values);
                    values.clear();
                }
            },
            Err(err) => {
                eprintln!("Error reading CSV: {}", err);
                continue;
            }
        }
    }

    if !values.is_empty() {
        insert_batch(&values);
    }

    // Commit the transaction.
    commit_transaction();

    println!("Data loaded successfully.");
}

// Helper function to batch insert values into the database.
fn insert_batch(values: &Vec<String>) {
    let sql_command = format!(
        "INSERT INTO btcusdt (tradeId, price, qty, quoteQty, time, isBuyerMaker) VALUES {}",
        values.join(", ")
    );

    let output = Command::new("mysql")
        .arg("--login-path=client")
        .arg("-e")
        .arg(&sql_command)
        .arg("binance_futures")
        .output()
        .expect("Failed to execute command");

    if !output.status.success() {
        eprintln!("Error: {}", String::from_utf8_lossy(&output.stderr));
    }
}

// Helper function to start a transaction in the database.
fn start_transaction() {
    let cmd = "START TRANSACTION;";
    Command::new("mysql")
        .arg("--login-path=client")
        .arg("-e")
        .arg(cmd)
        .arg("binance_futures")
        .output()
        .expect("Failed to start transaction");
}

// Helper function to commit a transaction in the database.
fn commit_transaction() {
    let cmd = "COMMIT;";
    Command::new("mysql")
        .arg("--login-path=client")
        .arg("-e")
        .arg(cmd)
        .arg("binance_futures")
        .output()
        .expect("Failed to commit transaction");
}

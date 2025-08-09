use mensa_api::cache::Cache;
use serde_json;
use std::fs::File;
use std::io::Write;

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Fetch the data
    let menu_data = Cache::fetch_data().await;
    let menu = menu_data.unwrap();
    let meals = menu.get_meals();

    // Convert to JSON
    let json_str = serde_json::to_string_pretty(&meals)?;

    // Write to a file
    let mut file = File::create("menu.json")?;
    file.write_all(json_str.as_bytes())?;

    println!("Menu saved as menu.json");
    Ok(())
}


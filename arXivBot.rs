use std::fs::File;
use std::io::Read;
use std::process;

use chrono::{Datelike, Duration, Local, TimeZone};
use chrono_tz::US::Eastern;
use tokio::runtime::Runtime;
use reqwest::blocking::Client;
use reqwest::Url;
use serde::Deserialize;
use serde_yaml;
use clap::Parser;

#[derive(Parser)]
struct Args {
    #[clap(short, long, default_value = "params.yaml")]
    params: String,
}

#[derive(Debug, Deserialize)]
struct Params {
    username: String,
    password: String,
    identifier: String,
    #[serde(default)]
    redirect_after_login: Option<String>,
}

fn main() {
    // Parse arguments
    let args = Args::parse();

    // Load parameters
    let mut file = File::open(&args.params).unwrap_or_else(|_| {
        eprintln!("Failed to open params file: {}", &args.params);
        process::exit(1);
    });
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    let params: Params = serde_yaml::from_str(&contents).unwrap();

    // Create HTTP client
    let client = Client::builder()
        .cookie_store(true)
        .build()
        .unwrap();

    // Login to arXiv
    println!("Logging in...");
    let base_url = "https://arxiv.org";
    let login_url = Url::parse(&format!("{}/login", base_url)).unwrap();
    let next_page = params.redirect_after_login.clone().unwrap_or_else(|| "https://arxiv.org/user".to_string());
    let mut login_data = std::collections::HashMap::new();
    login_data.insert("username", params.username.as_str());
    login_data.insert("password", params.password.as_str());
    login_data.insert("next_page", next_page.as_str());

    let response = client.post(login_url)
        .form(&login_data)
        .send()
        .unwrap();

    let text = response.text().unwrap();
    if !text.to_lowercase().contains("logout") {
        eprintln!("Login failed - check credentials");
        process::exit(1);
    }
    println!("Login successful");

    // Make relevant URLs
    let mut paper_url = Url::parse(base_url).unwrap();
    paper_url = paper_url.join("submit/").unwrap();
    paper_url = paper_url.join(&format!("{}/", params.identifier)).unwrap();
    let preview_url = paper_url.join("preview").unwrap();
    let submission_url = paper_url.join("submit").unwrap();

    // Test that we can access the submission page
    let response = client.get(preview_url.clone()).send().unwrap();
    if response.status() != 200 {
        eprintln!(
            "Failed to access submission page ({}): {}",
            preview_url, response.status()
        );
        process::exit(1);
    }
    println!("Access to submission page confirmed");
    
    // Get current time in ET
    let now_et = Eastern.from_utc_datetime(&Local::now().naive_utc());

    // Build 14:00 ET today
    let today_14_et = Eastern
        .with_ymd_and_hms(now_et.year(), now_et.month(), now_et.day(), 14, 0, 0)
        .unwrap();  // unwrap is safe since 14:00 is always valid

    // Determine if we need to schedule for tomorrow
    let target_et = if now_et >= today_14_et {
        today_14_et + Duration::days(1)
    } else {
        today_14_et
    };

    // Convert target ET time to local time
    let target_local = target_et.with_timezone(&Local);

    // Print waiting message
    println!(
        "Waiting until {} to submit...",
        target_local.format("%Y-%m-%d %H:%M:%S")
    );

    let rt = Runtime::new().unwrap();
    rt.block_on(async {
        // Tight spin loop with yield
        while Local::now() < target_local {
            tokio::task::yield_now().await;
        }
    });

    let mut submit_data = std::collections::HashMap::new();
    submit_data.insert("Submit", "Submit");
    let response = client.post(submission_url)
        .form(&submit_data)
        .send()
        .unwrap();
    println!("Submission response: {}", response.status());
    println!("Submission sent at: {}", Local::now().format("%Y-%m-%d %H:%M:%S%.6f"));

}
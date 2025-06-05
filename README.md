# arXiv Bot

This project automates the process of submitting a paper to arXiv at a specific hour. It supports both Python and Rust implementations.

## What does it do?

- Logs in to the arXiv submission website using your credentials.
- Navigates to your paper’s submission page.
- Waits until the 14:00 ET.
- Submits your paper automatically at the top of that hour.

**Note:** Your arXiv password is stored in plain text in params.yaml. Use with caution.

## Setup

1. **Install dependencies**  
   Use [pixi](https://pixi.sh/) to install all required dependencies:
   ```sh
   pixi install
   ```

2. **Configure your parameters**  
   Edit params.yaml with your arXiv username, password, and paper identifier.

   Example:
   ```yaml
   username: your_arxiv_username
   password: your_arxiv_password
   identifier: XXXXXX # arXiv paper identifier (do not include 'submit/')
   ```

## Running the Bot

### Python Version

The Python script is simple to use and requires no compilation.

```sh
pixi run python arXivBot.py
```

You can specify a custom parameters file with:
```sh
pixi run python arXivBot.py --params custom_params.yaml
```

### Rust Version

The Rust version is faster but requires compilation.

1. **Build the binary:**
   ```sh
   pixi run build
   ```

2. **Run the bot:**
   ```sh
   pixi run ./target/release/arXivBot
   ```
   Or, if you want to specify a custom parameters file:
   ```sh
   pixi run ./target/release/arXivBot --params custom_params.yaml
   ```

## How it works

- Both scripts log in to arXiv using your credentials.
- They check access to your paper’s submission page.
- The script waits in a loop until the specified hour.
- At the correct time, it submits your paper and prints the response status.

## Security Note

Your arXiv password is stored in plain text in params.yaml. Do not share this file and consider deleting it after use.

---

Let me know if you want this inserted into your README.md.
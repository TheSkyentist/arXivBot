arXiv Bot
=========

1. Install dependencies (pixi.toml)
2. Configure for your paper and arXiv account (params.yaml)
3. Run the script (arXivBot.py)

This script logs in to the arXiv submission website with a specific email and password, and submits a paper for publication. 

The script then searches for the submit button and enters into a loop that continuously checks the current time. At the top of the given hour, the script clicks the submit button and prints "Submitting!" to the console. Make sure you configure the hour to be appropriate for your local time. 

Final note: This script requires keeping your password in plain text. Until we get an arXiv API, this is the best I can do. 
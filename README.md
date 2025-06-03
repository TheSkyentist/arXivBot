arXiv Bot
=========

1. Create pixi or mamba/conda environment (pixi.toml or environment.yaml)
2. Configure for your paper and arXiv account (params.yaml)
3. Run the script (arXivBot.py)

This script logs in to the arXiv submission website with a specific email and password, and submits a paper for publication. I would not advise running this script with less than a minute to go until submission time. I usually run it about an hour before. 

The script opens a Google Chrome web browser using chromedriver, navigates to the submission preview page of arXiv, and fills in the email and password fields. It then clicks the "sign in" button and waits for 10 seconds. This script requires the Selenium package in order to interact with Google Chrome. 

The script then searches for the submit button and enters into a loop that continuously checks the current time. At the top of the given hour, the script clicks the submit button and prints "Submitting!" to the console. Make sure you configure the hour to be appropriate for your local time. 

You can install Selenium through conda or pip. You can install chromedriver through the following [link](https://chromedriver.chromium.org/downloads).
Important! Your versions of chromedriver and Google Chrome must be compatible, or the script will not work. 

Final note: This script requires keeping your password in plain text. Until we get an arXiv API, this is the best I can do. 
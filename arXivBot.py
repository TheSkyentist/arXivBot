#! /usr/bin/env python

# Import Packages
import os
import time
import yaml
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--params',default='params.yaml', help='Path to the parameters file')
args = parser.parse_args()

# Load parameters
with open(args.params) as f: params = yaml.safe_load(f)

# Use the installed chromedriver to automate chrome
# IF THIS LINE DOESN'T RUN, CHROMEDRIVER and CHROME VERSIONS ARE MISMATCHED
service = webdriver.ChromeService(executable_path=params['chromedriver']) 
driver = webdriver.Chrome(service=service)

# Open the webpage in Google Chrome
driver.get(params['paperlink'])

# Fill in email and password
emailField = WebDriverWait(driver, 20).until(
    ec.presence_of_element_located((By.ID, 'username'))
)
emailField.send_keys(params['username'])

pwField = WebDriverWait(driver, 20).until(
    ec.presence_of_element_located((By.ID, 'password'))
)
pwField.send_keys(params['password'])

# Click sign in button
driver.find_element('xpath','/html/body/main/content/div/div/form/fieldset/div[3]/div/input').click()

# Wait for webpage to load
time.sleep(10)

# Find the submit button
submitBtn = driver.find_element('xpath','/html/body/div[3]/div[3]/div[2]/div[3]/form/input')

# # Wait for hour to be correct
# while datetime.now().hour != params['hour']:

#     time.sleep(0.01) # Approximately minimum time we can go without being inaccurate due to OS timekeeping

# # Click the submit button
# submitBtn.click()
# print(f'Submitting! {datetime.datetime.now()}')

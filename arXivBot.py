#!/usr/bin/env python3

import time
import yaml
import requests
import argparse
from datetime import datetime, timedelta
from urllib.parse import urljoin
import pytz

# Constants
BASE_URL = 'https://arxiv.org'
ET = pytz.timezone('US/Eastern')
TARGET_HOUR_ET = 14

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--params', default='params.yaml', help='Path to the parameters file')
args = parser.parse_args()

# Load YAML parameters
with open(args.params) as f:
    params = yaml.safe_load(f)

# Create session
session = requests.Session()

# Login
print('Logging in...')
login_url = urljoin(BASE_URL, 'login')
login_data = {
    'username': params['username'],
    'password': params['password'],
    'next_page': params.get('redirect_after_login', 'https://arxiv.org/user'),
}
response = session.post(login_url, data=login_data)

if 'logout' not in response.text.lower():
    raise Exception('Login failed - check credentials')
print('Login successful')

# Build submission URLs
paper_url = BASE_URL
for part in ['submit', params['identifier']]:
    paper_url = urljoin(paper_url, f'{part}/')
preview_url = urljoin(paper_url, 'preview')
submission_url = urljoin(paper_url, 'submit')

# Verify submission access
response = session.get(preview_url)
if response.status_code != 200:
    raise Exception(f'Cannot access preview page ({preview_url}): {response.status_code}')
print('Access to submission page confirmed')

# Calculate next 14:00 ET
now_et = datetime.now(pytz.utc).astimezone(ET)
target_et = now_et.replace(hour=TARGET_HOUR_ET, minute=0, second=0, microsecond=0)

if now_et >= target_et:
    target_et += timedelta(days=1)

# Convert to local time for printing
local_time = target_et.astimezone()
print(f"Waiting until {local_time.strftime('%Y-%m-%d %H:%M:%S')} to submit...")

# Sleep loop
while datetime.now(pytz.utc) < target_et:
    time.sleep(0.01)

# Submit
response = session.post(submission_url, data={'Submit': 'Submit'})
print('Submission response:', response.status_code)

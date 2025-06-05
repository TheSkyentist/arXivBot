#!/usr/bin/env python

# Packages
import time
import yaml
import requests
import argparse
from datetime import datetime
from urllib.parse import urljoin

# arXiv base URL
base_url = 'https://arxiv.org'

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    '-p', '--params', default='params.yaml', help='Path to the parameters file'
)
args = parser.parse_args()

# Load parameters
with open(args.params) as f:
    params = yaml.safe_load(f)

# Create session
session = requests.Session()

# Login to arXiv
print('Logging in...')
login_url = urljoin(base_url, 'login')
login_data = {
    'username': params['username'],
    'password': params['password'],
    'next_page': params.get('redirect_after_login', 'https://arxiv.org/user'),
}
response = session.post(login_url, data=login_data)

# Verify login
if 'logout' not in response.text.lower():
    raise Exception('Login failed - check credentials')
print('Login successful')

# Make relevant URLs
paper_url = base_url
for part in ['submit', params['identifier']]:
    paper_url = urljoin(paper_url, f'{part}/')
preview_url = urljoin(paper_url, 'preview')
submission_url = urljoin(paper_url, 'submit')

# Test that we can access the submission page
response = session.get(preview_url)
if response.status_code != 200:
    raise Exception(
        f'Failed to access submission page ({preview_url}): {response.status_code}'
    )
print('Access to submission page confirmed')

# Wait for correct hour
print(f'Waiting until hour {params["hour"]}...')
while datetime.now().hour != params['hour']:
    time.sleep(0.01)

response = session.post(submission_url, data={'Submit': 'Submit'})
print('Submission response:', response.status_code)

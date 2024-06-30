import os
import json
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REPO_FILE = os.path.expanduser('~/.skufpkg/repositories.json')

def load_repositories():
    try:
        if os.path.exists(REPO_FILE):
            with open(REPO_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f'Error loading repositories: {e}')
        return []

def save_repositories(repositories):
    try:
        os.makedirs(os.path.dirname(REPO_FILE), exist_ok=True)
        with open(REPO_FILE, 'w') as f:
            json.dump(repositories, f)
    except Exception as e:
        logger.error(f'Error saving repositories: {e}')

def add_repository(url):
    repositories = load_repositories()
    if url not in repositories:
        repositories.append(url)
        save_repositories(repositories)
        logger.info(f'Repository {url} added.')
    else:
        logger.info(f'Repository {url} already exists.')

def list_repositories():
    repositories = load_repositories()
    for repo in repositories:
        print(repo)

def search_packages(package_name):
    repositories = load_repositories()
    for repo in repositories:
        try:
            url = f'{repo}/{package_name}.json'
            response = requests.get(url)
            if response.status_code == 200:
                print(f'Package found: {url}')
                return
        except Exception as e:
            logger.error(f'Error searching for package {package_name}: {e}')
    logger.info(f'Package {package_name} not found in any repository.')


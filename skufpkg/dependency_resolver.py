import os
import json
import logging
from skufpkg.package import install_package

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEPENDENCY_FILE = os.path.expanduser('~/.skufpkg/dependencies.json')

def load_dependencies():
    try:
        if os.path.exists(DEPENDENCY_FILE):
            with open(DEPENDENCY_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f'Error loading dependencies: {e}')
        return {}

def save_dependencies(dependencies):
    try:
        os.makedirs(os.path.dirname(DEPENDENCY_FILE), exist_ok=True)
        with open(DEPENDENCY_FILE, 'w') as f:
            json.dump(dependencies, f)
    except Exception as e:
        logger.error(f'Error saving dependencies: {e}')

def resolve_dependencies(package_name):
    dependencies = load_dependencies()
    if package_name in dependencies:
        for dependency in dependencies[package_name]:
            install_package(dependency)
        logger.info(f'Dependencies for {package_name} resolved.')
    else:
        logger.info(f'No dependencies found for {package_name}.')


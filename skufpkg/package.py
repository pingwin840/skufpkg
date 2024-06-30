import os
import tarfile
import requests
import json
import logging
from skufpkg.repository import load_repositories
from skufpkg.dependency_resolver import resolve_dependencies

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INSTALL_DIR = os.path.expanduser('~/.skufpkg/installed')
PACKAGE_META = os.path.expanduser('~/.skufpkg/package_meta.json')

def load_installed_packages():
    try:
        if os.path.exists(PACKAGE_META):
            with open(PACKAGE_META, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f'Error loading installed packages: {e}')
        return {}

def save_installed_packages(packages):
    try:
        os.makedirs(os.path.dirname(PACKAGE_META), exist_ok=True)
        with open(PACKAGE_META, 'w') as f:
            json.dump(packages, f)
    except Exception as e:
        logger.error(f'Error saving installed packages: {e}')

def install_package(package_name):
    repositories = load_repositories()
    for repo in repositories:
        url = f'{repo}/{package_name}.skufpkg'
        try:
            response = requests.get(url)
            response.raise_for_status()
            package_path = os.path.join(INSTALL_DIR, f'{package_name}.skufpkg')
            os.makedirs(INSTALL_DIR, exist_ok=True)
            with open(package_path, 'wb') as f:
                f.write(response.content)
            with tarfile.open(package_path) as tar:
                tar.extractall(INSTALL_DIR)
            package_meta = load_installed_packages()
            package_meta[package_name] = {
                'name': package_name,
                'version': 'unknown',  # To be updated after reading package metadata
            }
            save_installed_packages(package_meta)
            logger.info(f'Package {package_name} installed.')
            resolve_dependencies(package_name)
            return
        except requests.exceptions.RequestException as e:
            logger.error(f'Error downloading package {package_name}: {e}')
            continue
        except tarfile.TarError as e:
            logger.error(f'Error extracting package {package_name}: {e}')
            continue
    logger.error(f'Package {package_name} not found in any repository.')

def remove_package(package_name):
    package_path = os.path.join(INSTALL_DIR, f'{package_name}.skufpkg')
    if os.path.exists(package_path):
        try:
            os.remove(package_path)
            package_meta = load_installed_packages()
            if package_name in package_meta:
                del package_meta[package_name]
                save_installed_packages(package_meta)
            logger.info(f'Package {package_name} removed.')
        except Exception as e:
            logger.error(f'Error removing package {package_name}: {e}')
    else:
        logger.info(f'Package {package_name} is not installed.')

def list_installed_packages():
    packages = load_installed_packages()
    if packages:
        for package in packages:
            print(f"{package} - {packages[package]['version']}")
    else:
        logger.info('No packages installed.')

def create_package(source_dir, package_name, version):
    package_filename = f'{package_name}-{version}.skufpkg'
    try:
        with tarfile.open(package_filename, 'w:gz') as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        logger.info(f'Package created: {package_filename}')
    except Exception as e:
        logger.error(f'Error creating package {package_filename}: {e}')


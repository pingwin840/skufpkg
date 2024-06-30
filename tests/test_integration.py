import unittest
import os
import json
import tempfile
from unittest.mock import patch
from skufpkg.repository import add_repository, list_repositories, load_repositories, save_repositories
from skufpkg.package import install_package, remove_package, list_installed_packages, create_package
from skufpkg.dependency_resolver import load_dependencies, save_dependencies, resolve_dependencies

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.test_repo_file = tempfile.NamedTemporaryFile(delete=False).name
        self.test_dependency_file = tempfile.NamedTemporaryFile(delete=False).name
        self.test_install_dir = tempfile.mkdtemp()
        self.test_package_meta = tempfile.NamedTemporaryFile(delete=False).name
        
        self.original_repo_file = skufpkg.repository.REPO_FILE
        self.original_dependency_file = skufpkg.dependency_resolver.DEPENDENCY_FILE
        self.original_install_dir = skufpkg.package.INSTALL_DIR
        self.original_package_meta = skufpkg.package.PACKAGE_META
        
        skufpkg.repository.REPO_FILE = self.test_repo_file
        skufpkg.dependency_resolver.DEPENDENCY_FILE = self.test_dependency_file
        skufpkg.package.INSTALL_DIR = self.test_install_dir
        skufpkg.package.PACKAGE_META = self.test_package_meta
        
        self.repo_url = "http://localhost:5000"
        add_repository(self.repo_url)

        self.package_name = "test-package"
        self.package_version = "1.0"
        self.package_filename = f"{self.package_name}-{self.package_version}.skufpkg"
        self.package_path = os.path.join(self.test_install_dir, self.package_filename)
        
        self.create_test_package()

    def tearDown(self):
        os.remove(self.test_repo_file)
        os.remove(self.test_dependency_file)
        os.rmdir(self.test_install_dir)
        os.remove(self.test_package_meta)
        
        skufpkg.repository.REPO_FILE = self.original_repo_file
        skufpkg.dependency_resolver.DEPENDENCY_FILE = self.original_dependency_file
        skufpkg.package.INSTALL_DIR = self.original_install_dir
        skufpkg.package.PACKAGE_META = self.original_package_meta

    def create_test_package(self):
        source_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(source_dir, 'test-dir'))
        with open(os.path.join(source_dir, 'test-dir', 'test-file.txt'), 'w') as f:
            f.write('test content')
        
        create_package(source_dir, self.package_name, self.package_version)
        os.rename(self.package_filename, self.package_path)

    @patch('skufpkg.package.requests.get')
    def test_install_package(self, mock_get):
        with open(self.package_path, 'rb') as f:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = f.read()
        
        install_package(self.package_name)
        installed_packages = skufpkg.package.load_installed_packages()
        self.assertIn(self.package_name, installed_packages)
        
        installed_files = os.listdir(os.path.join(self.test_install_dir, self.package_name))
        self.assertIn('test-dir', installed_files)

    def test_remove_package(self):
        install_package(self.package_name)
        remove_package(self.package_name)
        installed_packages = skufpkg.package.load_installed_packages()
        self.assertNotIn(self.package_name, installed_packages)

    def test_list_installed_packages(self):
        install_package(self.package_name)
        installed_packages = skufpkg.package.load_installed_packages()
        self.assertIn(self.package_name, installed_packages)

    @patch('skufpkg.package.install_package')
    def test_resolve_dependencies(self, mock_install_package):
        dependencies = {self.package_name: ["dependency1", "dependency2"]}
        save_dependencies(dependencies)
        resolve_dependencies(self.package_name)
        mock_install_package.assert_any_call('dependency1')
        mock_install_package.assert_any_call('dependency2')

if __name__ == '__main__':
    unittest.main()


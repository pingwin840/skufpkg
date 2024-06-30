import unittest
import os
from skufpkg.dependency_resolver import load_dependencies, save_dependencies, resolve_dependencies
from unittest.mock import patch

class TestDependencyResolver(unittest.TestCase):

    def setUp(self):
        self.dependency_file = '/tmp/test_dependencies.json'
        self.original_dependency_file = skufpkg.dependency_resolver.DEPENDENCY_FILE
        skufpkg.dependency_resolver.DEPENDENCY_FILE = self.dependency_file
        self.dependencies = {"packageA": ["dependency1", "dependency2"]}
        save_dependencies(self.dependencies)

    def tearDown(self):
        if os.path.exists(self.dependency_file):
            os.remove(self.dependency_file)
        skufpkg.dependency_resolver.DEPENDENCY_FILE = self.original_dependency_file

    @patch('skufpkg.package.install_package')
    def test_resolve_dependencies(self, mock_install_package):
        resolve_dependencies('packageA')
        mock_install_package.assert_any_call('dependency1')
        mock_install_package.assert_any_call('dependency2')

if __name__ == '__main__':
    unittest.main()


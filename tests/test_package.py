import unittest
import os
from skufpkg.package import install_package, remove_package, list_installed_packages, create_package
from unittest.mock import patch, MagicMock

class TestPackage(unittest.TestCase):

    def setUp(self):
        self.install_dir = '/tmp/test_installed'
        self.original_install_dir = skufpkg.package.INSTALL_DIR
        skufpkg.package.INSTALL_DIR = self.install_dir
        os.makedirs(self.install_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.install_dir):
            for file in os.listdir(self.install_dir):
                os.remove(os.path.join(self.install_dir, file))
            os.rmdir(self.install_dir)
        skufpkg.package.INSTALL_DIR = self.original_install_dir

    @patch('skufpkg.package.requests.get')
    def test_install_package(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'fake content'
        install_package('fake-package')
        self.assertTrue(os.path.exists(os.path.join(self.install_dir, 'fake-package.skufpkg')))

    def test_remove_package(self):
        package_path = os.path.join(self.install_dir, 'fake-package.skufpkg')
        with open(package_path, 'wb') as f:
            f.write(b'fake content')
        remove_package('fake-package')
        self.assertFalse(os.path.exists(package_path))

if __name__ == '__main__':
    unittest.main()


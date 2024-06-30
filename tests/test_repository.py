import unittest
from skufpkg.repository import add_repository, list_repositories, load_repositories, save_repositories
import os
import json

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.test_repo_file = '/tmp/test_repositories.json'
        self.original_repo_file = skufpkg.repository.REPO_FILE
        skufpkg.repository.REPO_FILE = self.test_repo_file
        self.repositories = ["http://example.com/repo1", "http://example.com/repo2"]
        save_repositories(self.repositories)

    def tearDown(self):
        if os.path.exists(self.test_repo_file):
            os.remove(self.test_repo_file)
        skufpkg.repository.REPO_FILE = self.original_repo_file

    def test_add_repository(self):
        new_repo = "http://example.com/repo3"
        add_repository(new_repo)
        repos = load_repositories()
        self.assertIn(new_repo, repos)

    def test_list_repositories(self):
        repos = load_repositories()
        self.assertEqual(repos, self.repositories)

if __name__ == '__main__':
    unittest.main()


import unittest
from github import GitHub

class TestGitHub(unittest.TestCase):
    def setUp(self):
        self.github = GitHub()

    def test_get_user(self):
        user = self.github.get_user()
        self.assertIn("login", user)

if __name__ == "__main__":
    unittest.main()
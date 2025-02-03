import unittest
import os
from src.Github import GitHub

class TestGitHub(unittest.TestCase):
    def setUp(self):
        if not os.path.isfile('.env'):
            self.skipTest("No tenim fitxer .env. Test skiped")
        
        self.github = GitHub()

    def test_get_user(self):
        user = self.github.get_user()
        self.assertIn("login", user)

if __name__ == "__main__":
    unittest.main()

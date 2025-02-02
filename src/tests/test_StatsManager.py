import unittest
from unittest.mock import patch
from src.modules.StatsManager import StatsManager

class TestStatsManager(unittest.TestCase):
    
    def setUp(self):
        self.stats_manager = StatsManager()

    @patch("requests.get")
    def test_get_repo_stats(self, mock_get):
        mock_get.return_value.json.return_value = [{"author": {"login": "user1"}, "total": 42}]
        response = self.stats_manager.get_repo_stats("owner", "repo")
        self.assertEqual(response[0]["total"], 42)

    @patch("requests.get")
    def test_get_repo_commits(self, mock_get):
        mock_get.return_value.json.return_value = [{"commit": {"message": "Initial commit"}}]
        response = self.stats_manager.get_repo_commits("owner", "repo")
        self.assertEqual(response[0]["commit"]["message"], "Initial commit")

    @patch("requests.get")
    def test_get_repo_issues(self, mock_get):
        mock_get.return_value.json.return_value = [{"title": "Bug report"}]
        response = self.stats_manager.get_repo_issues("owner", "repo")
        self.assertEqual(response[0]["title"], "Bug report")

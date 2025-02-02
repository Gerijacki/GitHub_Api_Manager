import unittest
from unittest.mock import patch, MagicMock
from src.modules.RepoManager import RepoManager

class TestRepoManager(unittest.TestCase):
    
    def setUp(self):
        self.repo_manager = RepoManager()

    @patch("src.modules.RepoManager.RepoManager._handle_request")
    def test_create_repo(self, mock_request):
        mock_request.return_value = {"id": 123, "name": "test-repo"}
        response = self.repo_manager.create_repo("test-repo")
        self.assertEqual(response["name"], "test-repo")

    @patch("src.modules.RepoManager.RepoManager._handle_request")
    def test_delete_repo(self, mock_request):
        mock_request.return_value = {}
        response = self.repo_manager.delete_repo("test-repo")
        self.assertTrue(response)

    @patch("src.modules.RepoManager.RepoManager._handle_request")
    def test_create_branch(self, mock_request):
        mock_request.side_effect = [
            {"object": {"sha": "123abc"}},
            {"ref": "refs/heads/new-branch"}
        ]
        response = self.repo_manager.create_branch("test-repo", "new-branch")
        self.assertEqual(response["ref"], "refs/heads/new-branch")

    @patch("src.modules.RepoManager.RepoManager._handle_request")
    def test_merge_branches(self, mock_request):
        mock_request.return_value = {"merged": True}
        response = self.repo_manager.merge_branches("test-repo", "main", "feature-branch")
        self.assertTrue(response["merged"])

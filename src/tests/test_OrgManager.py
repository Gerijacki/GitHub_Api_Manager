import unittest
from unittest.mock import patch, MagicMock
from src.Github import GitHub
from src.modules.OrgManager import OrgManager

class TestOrgManager(unittest.TestCase):
    
    def setUp(self):
        self.org_manager = OrgManager()

    @patch("src.modules.OrgManager.requests.get")
    def test_list_orgs(self, mock_get):
        mock_get.return_value.json.return_value = [{"login": "org1"}, {"login": "org2"}]
        
        response = self.org_manager.list_orgs()
        
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["login"], "org1")
        self.assertEqual(response[1]["login"], "org2")

    @patch("src.modules.OrgManager.requests.get")
    def test_get_org_details(self, mock_get):
        mock_get.return_value.json.return_value = {"name": "org1", "description": "Una organització"}
        
        response = self.org_manager.get_org_details("org1")
        
        self.assertEqual(response["name"], "org1")
        self.assertEqual(response["description"], "Una organització")

    @patch("src.modules.OrgManager.requests.get")
    def test_list_org_members(self, mock_get):
        mock_get.return_value.json.return_value = [{"login": "user1"}, {"login": "user2"}]
        
        response = self.org_manager.list_org_members("org1")
        
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["login"], "user1")
        self.assertEqual(response[1]["login"], "user2")

    @patch("src.modules.OrgManager.requests.put")
    def test_add_member_to_org(self, mock_put):
        mock_put.return_value.json.return_value = {"state": "active"}
        
        response = self.org_manager.add_member_to_org("org1", "user1")
        
        self.assertEqual(response["state"], "active")

    @patch("src.modules.OrgManager.requests.delete")
    def test_remove_member_from_org(self, mock_delete):
        mock_delete.return_value.status_code = 204
        
        response = self.org_manager.remove_member_from_org("org1", "user1")
        
        self.assertTrue(response)

    @patch("src.modules.OrgManager.requests.get")
    def test_list_org_repos(self, mock_get):
        mock_get.return_value.json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        
        response = self.org_manager.list_org_repos("org1")
        
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["name"], "repo1")
        self.assertEqual(response[1]["name"], "repo2")

    @patch("src.modules.OrgManager.requests.post")
    def test_create_org_repo(self, mock_post):
        mock_post.return_value.json.return_value = {"id": 123, "name": "test-repo"}
        
        response = self.org_manager.create_org_repo("org1", "test-repo")
        
        self.assertEqual(response["name"], "test-repo")

if __name__ == '__main__':
    unittest.main()

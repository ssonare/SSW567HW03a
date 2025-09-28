# test_github_api.py
import unittest
from unittest.mock import patch
import github_api

class TestGitHubAPI(unittest.TestCase):

    @patch("github_api.requests.get")
    def test_valid_user_with_repos(self, mock_get):
        # Mock response for repos
        mock_get.side_effect = [
            # First call -> user repos
            MockResponse([{"name": "Repo1"}, {"name": "Repo2"}], 200),
            # Second call -> commits for Repo1
            MockResponse([{}, {}, {}], 200),  # 3 commits
            # Third call -> commits for Repo2
            MockResponse([{}, {}], 200),  # 2 commits
        ]

        result = github_api.get_user_repo_commits("fakeuser")
        self.assertEqual(result, [("Repo1", 3), ("Repo2", 2)])

    @patch("github_api.requests.get")
    def test_invalid_user(self, mock_get):
        mock_get.return_value = MockResponse(None, 404)
        with self.assertRaises(ValueError):
            github_api.get_user_repo_commits("invaliduser")


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    
    def json(self):
        return self.json_data


if __name__ == "__main__":
    unittest.main()

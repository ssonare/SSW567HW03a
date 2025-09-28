# github_api.py
import requests

def get_user_repo_commits(user_id):
    """
    Given a GitHub user ID, return a list of tuples with repo name and commit count.
    Example: [("Triangle567", 10), ("Square567", 27)]
    """
    repos_url = f"https://api.github.com/users/{user_id}/repos"
    response = requests.get(repos_url)
    
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve repos for user {user_id}, status code {response.status_code}")

    repos = response.json()
    repo_commit_counts = []

    for repo in repos:
        repo_name = repo["name"]
        commits_url = f"https://api.github.com/repos/{user_id}/{repo_name}/commits"
        commit_response = requests.get(commits_url)

        if commit_response.status_code != 200:
            commit_count = 0  # fallback if error occurs
        else:
            commits = commit_response.json()
            commit_count = len(commits)

        repo_commit_counts.append((repo_name, commit_count))

    return repo_commit_counts


if __name__ == "__main__":
    # Simple demo run
    results = get_user_repo_commits("richkempinski")
    for repo, commits in results:
        print(f"Repo: {repo} Number of commits: {commits}")

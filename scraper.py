import requests
from bs4 import BeautifulSoup


class GitHubScraper:
    def __init__(self, token=None):
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})

    def get_user_repos(self, username):
        """Fetch all repos of a user via GitHub API with pagination"""
        url = f"{self.base_url}/users/{username}/repos"
        repos = []
        while url:
            resp = self.session.get(url)
            resp.raise_for_status()
            repos.extend(resp.json())
            # Handle pagination
            url = resp.links.get("next", {}).get("url")
        return [
            {
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "url": repo["html_url"]
            }
            for repo in repos
        ]

    def scrape_html_repos(self, username):
        """Fallback scraper using HTML"""
        url = f"https://github.com/{username}?tab=repositories"
        resp = self.session.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        repos = soup.find_all("a", itemprop="name codeRepository")

        return [
            {"name": repo.text.strip(), "url": "https://github.com" + repo["href"]}
            for repo in repos
        ]

import os
from dotenv import load_dotenv
from scraper import GitHubScraper
from export import save_to_csv, save_to_json


def run_scraper():
    # Load environment variables
    load_dotenv()

    username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")

    if not username:
        raise ValueError("GITHUB_USERNAME is not set in .env")

    scraper = GitHubScraper(token=token)

    # Try API first
    try:
        repos = scraper.get_user_repos(username)
    except Exception as e:
        print(f"API failed, falling back to HTML: {e}")
        repos = scraper.scrape_html_repos(username)

    print(f"Found {len(repos)} repositories for {username}")
    for repo in repos:
        print(f"{repo['name']} -> {repo['url']}")

    # Export results
    save_to_csv(repos, f"{username}_repos.csv")
    save_to_json(repos, f"{username}_repos.json")
    print("Data saved to CSV and JSON.")


if __name__ == "__main__":
    run_scraper()

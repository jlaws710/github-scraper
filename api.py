from fastapi import FastAPI, HTTPException
from scraper import GitHubScraper

app = FastAPI(title="GitHub Scraper API")


@app.get("/repos/{username}")
def get_user_repos(username: str, token: str | None = None):
    """
    Fetch GitHub repositories for a username.
    Optional: pass ?token=YOUR_GITHUB_TOKEN to avoid rate limits.
    """
    scraper = GitHubScraper(token=token)

    try:
        repos = scraper.get_user_repos(username)
    except Exception as e:
        # fallback to HTML scraping
        try:
            repos = scraper.scrape_html_repos(username)
        except Exception:
            raise HTTPException(status_code=500, detail=f"Failed to fetch repos: {str(e)}")

    if not repos:
        raise HTTPException(status_code=404, detail="No repositories found")

    return {"username": username, "repo_count": len(repos), "repositories": repos}

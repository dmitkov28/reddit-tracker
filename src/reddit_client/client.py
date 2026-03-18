from typing import Optional
import httpx

from src._types import RedditResponse
from src.model import ThreadClean


class RedditClient:
    base_url = "https://www.reddit.com"

    def __init__(self, client: Optional[httpx.Client] = None) -> None:
        self._http = client or httpx.Client()

    def _build_url(self, subreddit: str) -> str:
        return f"{self.base_url}/r/{subreddit}/new.json"

    def _process_threads(self, response: RedditResponse):
        threads = response["data"]["children"]
        return [
            ThreadClean(
                title=thread["data"]["title"],
                selftext=thread["data"]["selftext"],
                created=thread["data"]["created"],
                author=thread["data"]["author"],
            )
            for thread in threads
        ]

    def fetch_threads_for_subreddit(self, subreddit: str, limit: int = 100):
        res = self._http.get(
            url=self._build_url(subreddit=subreddit), params={"limit": limit}
        )
        res_json: RedditResponse = res.json()
        return self._process_threads(response=res_json)

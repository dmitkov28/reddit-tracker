from typing import Optional
import httpx

from src._types import RedditThreadResponse
from src._types._comments import RedditCommentResponse
from src.model import Comment, ThreadClean
from src.logger import logger


class RedditClient:
    base_url = "https://www.reddit.com"

    def __init__(self, client: Optional[httpx.Client] = None) -> None:
        self._http = client or httpx.Client()

    def _build_thread_url(self, subreddit: str) -> str:
        return f"{self.base_url}/r/{subreddit}/new.json"

    def _build_comments_url(self, subreddit: str) -> str:
        return f"{self.base_url}/r/{subreddit}/comments.json"

    @property
    def _headers(self) -> dict:
        headers = {
            "Host": "www.reddit.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:147.0) Gecko/20100101 Firefox/147.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Connection": "keep-alive",
            "Priority": "u=0, i",
            "TE": "trailers",
        }
        return headers

    def _process_threads(self, response: RedditThreadResponse):
        threads = response["data"]["children"]
        return [
            ThreadClean(
                id=thread["data"]["id"],
                title=thread["data"]["title"],
                selftext=thread["data"]["selftext"],
                created=thread["data"]["created"],
                author=thread["data"]["author"],
                comments=thread["data"]["num_comments"],
                upvotes=thread["data"]["ups"],
                permalink=thread["data"]["permalink"],
            )
            for thread in threads
        ]

    def _process_comments(self, response: RedditCommentResponse):
        comments = response["data"]["children"]
        return [
            Comment(
                id=comment["id"],
                thread_id=comment["parent_id"].removeprefix("t3_"),
                permalink=comment["permalink"],
                upvotes=comment["ups"],
                text=comment["body"],
                created=comment["created"],
                author=comment["author"],
            )
            for comment in comments
        ]

    def fetch_threads_for_subreddit(self, subreddit: str, limit: int = 100):
        url = self._build_thread_url(subreddit=subreddit)
        logger.info(f"Fetching {url}")
        res = self._http.get(url=url, params={"limit": limit}, headers=self._headers)
        logger.info(f"Status: {res.status_code}")
        res.raise_for_status()
        res_json: RedditThreadResponse = res.json()
        return self._process_threads(response=res_json)

    def fetch_comments_for_subreddit(self, subreddit: str, limit: int = 100):
        url = self._build_comments_url(subreddit=subreddit)
        logger.info(f"Fetching {url}")
        res = self._http.get(url=url, params={"limit": limit}, headers=self._headers)
        logger.info(f"Status: {res.status_code}")
        res.raise_for_status()
        res_json: RedditCommentResponse = res.json()
        return self._process_comments(response=res_json)

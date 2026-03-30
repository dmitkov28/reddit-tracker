from unittest.mock import Mock

import httpx

from src._types._comments import CommentChild, RedditCommentResponse
from src._types._threads import Children, RedditThreadResponse
from src.reddit_client.client import RedditClient
import pytest

from src.model import ThreadClean, Comment


def test_build_thread_url():
    c = RedditClient(client=Mock())
    assert c._build_thread_url("test") == "https://www.reddit.com/r/test/new.json"


def test_build_comments_url():
    c = RedditClient(client=Mock())
    assert (
        c._build_comments_url("test") == "https://www.reddit.com/r/test/comments.json"
    )


def test_custom_headers():
    c = RedditClient(client=Mock())
    assert c._headers == {
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


def _thread_response(children: Children) -> RedditThreadResponse:
    return {
        "kind": "Listing",
        "data": {
            "after": "",
            "dist": len(children),
            "modhash": "",
            "geo_filter": "",
            "children": children,  # type: ignore
        },
    }


def _thread_child(
    id="1",
    title="t",
    selftext="",
    created=1.0,
    author="a",
    num_comments=0,
    ups=0,
    permalink="/r/test",
):
    return {
        "kind": "t3",
        "data": {
            "id": id,
            "title": title,
            "selftext": selftext,
            "created": created,
            "author": author,
            "num_comments": num_comments,
            "ups": ups,
            "permalink": permalink,
        },
    }


def _comment_response(children: list[CommentChild]) -> RedditCommentResponse:
    return {
        "kind": "Listing",
        "data": {"after": None, "dist": len(children), "children": children},
    }


def _comment_child(
    id="c1",
    link_id="t3_abc",
    permalink="/r/test/comment",
    ups=0,
    body="hello",
    created=1.0,
    author="a",
):
    return {
        "kind": "t1",
        "data": {
            "id": id,
            "link_id": link_id,
            "permalink": permalink,
            "ups": ups,
            "body": body,
            "created": created,
            "author": author,
        },
    }


@pytest.mark.parametrize(
    "children,expected",
    [
        ([], []),
        (
            [_thread_child(id="1", title="First", ups=10)],
            [
                ThreadClean(
                    id="1",
                    title="First",
                    selftext="",
                    created=1.0,
                    author="a",
                    comments=0,
                    upvotes=10,
                    permalink="/r/test",
                )
            ],
        ),
        (
            [_thread_child(id="1"), _thread_child(id="2", author="b")],
            [
                ThreadClean(
                    id="1",
                    title="t",
                    selftext="",
                    created=1.0,
                    author="a",
                    comments=0,
                    upvotes=0,
                    permalink="/r/test",
                ),
                ThreadClean(
                    id="2",
                    title="t",
                    selftext="",
                    created=1.0,
                    author="b",
                    comments=0,
                    upvotes=0,
                    permalink="/r/test",
                ),
            ],
        ),
    ],
)
def test_process_threads(children, expected):
    c = RedditClient(client=Mock())
    result = c._process_threads(_thread_response(children))
    assert result == expected


@pytest.mark.parametrize(
    "children,expected",
    [
        ([], []),
        (
            [_comment_child(id="c1", link_id="t3_abc", body="hi", ups=5)],
            [
                Comment(
                    id="c1",
                    thread_id="abc",
                    permalink="/r/test/comment",
                    upvotes=5,
                    text="hi",
                    created=1.0,
                    author="a",
                )
            ],
        ),
        (
            [
                _comment_child(id="c1", link_id="t3_x"),
                _comment_child(id="c2", link_id="t3_y", author="b"),
            ],
            [
                Comment(
                    id="c1",
                    thread_id="x",
                    permalink="/r/test/comment",
                    upvotes=0,
                    text="hello",
                    created=1.0,
                    author="a",
                ),
                Comment(
                    id="c2",
                    thread_id="y",
                    permalink="/r/test/comment",
                    upvotes=0,
                    text="hello",
                    created=1.0,
                    author="b",
                ),
            ],
        ),
    ],
)
def test_process_comments(children, expected):
    c = RedditClient(client=Mock())
    result = c._process_comments(_comment_response(children))
    assert result == expected


def test_fetch_threads_for_subreddit():
    mock_response = {
        "kind": "Listing",
        "data": {
            "after": "t3_1s5ja3a",
            "dist": 2,
            "modhash": "",
            "geo_filter": None,
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "approved_at_utc": None,
                        "subreddit": "programming",
                        "selftext": "test",
                        "author_fullname": "t2_nn0q",
                        "saved": False,
                        "mod_reason_title": None,
                        "gilded": 0,
                        "clicked": False,
                        "title": "State of the Subreddit (January 2027): Mods applications and rules updates",
                        "link_flair_richtext": [],
                        "subreddit_name_prefixed": "r/programming",
                        "hidden": False,
                        "pwls": 6,
                        "link_flair_css_class": None,
                        "downs": 0,
                        "top_awarded_type": None,
                        "hide_score": False,
                        "name": "t3_1qoxwdt",
                        "quarantine": False,
                        "link_flair_text_color": "dark",
                        "upvote_ratio": 0.94,
                        "author_flair_background_color": None,
                        "subreddit_type": "public",
                        "ups": 123,
                        "total_awards_received": 0,
                        "media_embed": {},
                        "author_flair_template_id": None,
                        "is_original_content": False,
                        "user_reports": [],
                        "secure_media": None,
                        "is_reddit_media_domain": False,
                        "is_meta": False,
                        "category": None,
                        "secure_media_embed": {},
                        "link_flair_text": None,
                        "can_mod_post": False,
                        "score": 123,
                        "approved_by": None,
                        "is_created_from_ads_ui": False,
                        "author_premium": False,
                        "thumbnail": "",
                        "edited": 1769580556.0,
                        "author_flair_css_class": None,
                        "author_flair_richtext": [],
                        "gildings": {},
                        "content_categories": None,
                        "is_self": True,
                        "mod_note": None,
                        "created": 1769565254.0,
                        "link_flair_type": "text",
                        "wls": 6,
                        "removed_by_category": None,
                        "banned_by": None,
                        "author_flair_type": "text",
                        "domain": "self.programming",
                        "allow_live_comments": False,
                        "selftext_html": "test",
                        "likes": None,
                        "suggested_sort": None,
                        "banned_at_utc": None,
                        "view_count": None,
                        "archived": False,
                        "no_follow": False,
                        "is_crosspostable": False,
                        "pinned": False,
                        "over_18": False,
                        "all_awardings": [],
                        "awarders": [],
                        "media_only": False,
                        "can_gild": False,
                        "spoiler": False,
                        "locked": False,
                        "author_flair_text": None,
                        "treatment_tags": [],
                        "visited": False,
                        "removed_by": None,
                        "num_reports": None,
                        "distinguished": "moderator",
                        "subreddit_id": "t5_2fwo",
                        "author_is_blocked": False,
                        "mod_reason_by": None,
                        "removal_reason": None,
                        "link_flair_background_color": "",
                        "id": "1qoxwdt",
                        "is_robot_indexable": True,
                        "report_reasons": None,
                        "author": "ketralnis",
                        "discussion_type": None,
                        "num_comments": 91,
                        "send_replies": False,
                        "contest_mode": False,
                        "mod_reports": [],
                        "author_patreon_flair": False,
                        "author_flair_text_color": None,
                        "permalink": "/r/programming/comments/1qoxwdt/state_of_the_subreddit_january_2027_mods/",
                        "stickied": True,
                        "url": "https://www.reddit.com/r/programming/comments/1qoxwdt/state_of_the_subreddit_january_2027_mods/",
                        "subreddit_subscribers": 6858614,
                        "created_utc": 1769565254.0,
                        "num_crossposts": 0,
                        "media": None,
                        "is_video": False,
                    },
                },
            ],
            "before": None,
        },
    }

    def handler(req: httpx.Request):
        return httpx.Response(status_code=200, json=mock_response)

    mock_client = httpx.Client(transport=httpx.MockTransport(handler=handler))

    c = RedditClient(client=mock_client)
    res = c.fetch_threads_for_subreddit(subreddit="test")
    assert res == [
        ThreadClean(
            created=1769565254.0,
            id="1qoxwdt",
            title="State of the Subreddit (January 2027): Mods applications and rules updates",
            selftext="test",
            author="ketralnis",
            permalink="/r/programming/comments/1qoxwdt/state_of_the_subreddit_january_2027_mods/",
            comments=91,
            upvotes=123,
        )
    ]


def test_fetch_comments_for_subreddit():
    mock_response = {
        "kind": "Listing",
        "data": {
            "after": "t1_ocwz9q2",
            "dist": 1,
            "modhash": "",
            "geo_filter": "",
            "children": [
                {
                    "kind": "t1",
                    "data": {
                        "subreddit_id": "t5_2fwo",
                        "approved_at_utc": None,
                        "author_is_blocked": False,
                        "comment_type": None,
                        "link_title": "How I accidentally made the fastest C# CSV parser",
                        "mod_reason_by": None,
                        "banned_by": None,
                        "ups": 1,
                        "num_reports": None,
                        "author_flair_type": "text",
                        "total_awards_received": 0,
                        "subreddit": "programming",
                        "link_author": "big_bill_wilson",
                        "likes": None,
                        "replies": "",
                        "user_reports": [],
                        "saved": False,
                        "id": "ocwz9q2",
                        "banned_at_utc": None,
                        "mod_reason_title": None,
                        "gilded": 0,
                        "archived": False,
                        "collapsed_reason_code": None,
                        "no_follow": True,
                        "author": "aksdb",
                        "num_comments": 47,
                        "can_mod_post": False,
                        "send_replies": True,
                        "parent_id": "t1_ocwtnl5",
                        "score": 1,
                        "author_fullname": "t2_ns2t0p7",
                        "over_18": False,
                        "report_reasons": None,
                        "removal_reason": None,
                        "approved_by": None,
                        "controversiality": 0,
                        "body": "You could argue the same for client side JS code injection, yet auditors will demand of us to make sure we limit the risk of a client being exploited to a minimum so our backend has to sanitize as much as possible.\n\nSo now most of our profile fields can\u2019t contain or start with certain characters. Great, isn\u2019t it?",
                        "edited": False,
                        "top_awarded_type": None,
                        "downs": 0,
                        "author_flair_css_class": None,
                        "is_submitter": False,
                        "collapsed": False,
                        "author_flair_richtext": [],
                        "author_patreon_flair": False,
                        "body_html": '&lt;div class="md"&gt;&lt;p&gt;You could argue the same for client side JS code injection, yet auditors will demand of us to make sure we limit the risk of a client being exploited to a minimum so our backend has to sanitize as much as possible.&lt;/p&gt;\n\n&lt;p&gt;So now most of our profile fields can\u2019t contain or start with certain characters. Great, isn\u2019t it?&lt;/p&gt;\n&lt;/div&gt;',
                        "gildings": {},
                        "collapsed_reason": None,
                        "distinguished": None,
                        "associated_award": None,
                        "stickied": False,
                        "author_premium": False,
                        "can_gild": False,
                        "link_id": "t3_1s59ff3",
                        "unrepliable_reason": None,
                        "author_flair_text_color": None,
                        "score_hidden": False,
                        "permalink": "/r/programming/comments/1s59ff3/how_i_accidentally_made_the_fastest_c_csv_parser/ocwz9q2/",
                        "subreddit_type": "public",
                        "link_permalink": "https://www.reddit.com/r/programming/comments/1s59ff3/how_i_accidentally_made_the_fastest_c_csv_parser/",
                        "name": "t1_ocwz9q2",
                        "author_flair_template_id": None,
                        "subreddit_name_prefixed": "r/programming",
                        "author_flair_text": None,
                        "treatment_tags": [],
                        "created": 1774681028.0,
                        "created_utc": 1774681028.0,
                        "awarders": [],
                        "all_awardings": [],
                        "locked": False,
                        "author_flair_background_color": None,
                        "collapsed_because_crowd_control": None,
                        "mod_reports": [],
                        "quarantine": False,
                        "mod_note": None,
                        "link_url": "https://bepis.io/blog/turbo-csv-parser/",
                    },
                }
            ],
            "before": None,
        },
    }

    def handler(req: httpx.Request):
        return httpx.Response(status_code=200, json=mock_response)

    mock_client = httpx.Client(transport=httpx.MockTransport(handler=handler))

    c = RedditClient(client=mock_client)
    res = c.fetch_comments_for_subreddit(subreddit="test")
    assert res == [
        Comment(
            created=1774681028.0,
            id="ocwz9q2",
            thread_id="1s59ff3",
            text="You could argue the same for client side JS code injection, yet auditors will demand of us to make sure we limit the risk of a client being exploited to a minimum so our backend has to sanitize as much as possible.\n\nSo now most of our profile fields can’t contain or start with certain characters. Great, isn’t it?",
            author="aksdb",
            permalink="/r/programming/comments/1s59ff3/how_i_accidentally_made_the_fastest_c_csv_parser/ocwz9q2/",
            upvotes=1,
        )
    ]
